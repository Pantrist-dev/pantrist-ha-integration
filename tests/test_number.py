"""Pantry-amount number entity tests."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed, HomeAssistantError
from homeassistant.helpers import entity_registry as er
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.pantrist.api import PantristApiError, PantristAuthError
from custom_components.pantrist.const import DOMAIN
from custom_components.pantrist.coordinator import PantristCoordinator, PantristData
from custom_components.pantrist.list_manager import (
    signal_new_list,
    signal_pantry_items_changed,
)
from custom_components.pantrist.number import PantristPantryAmountNumber

from .conftest import LIST_ID, LIST_NAME


ITEM_UUID = "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"


def _make_coordinator(hass: HomeAssistant, data: PantristData) -> PantristCoordinator:
    coord = PantristCoordinator(hass, MagicMock(), MagicMock(), LIST_ID, LIST_NAME)
    coord.data = data
    return coord


def _make_entity(
    hass: HomeAssistant, *, amount: float | None = 3, unit_id: str | None = "kg"
) -> tuple[PantristPantryAmountNumber, PantristCoordinator]:
    items: list[dict[str, object]] = [
        {
            "uuid": ITEM_UUID,
            "name": "Pasta",
            "amount": amount,
            "unitId": unit_id,
        }
    ]
    coord = _make_coordinator(hass, PantristData(pantry={"items": items}))
    api = MagicMock()
    api.change_pantry_item_amount = AsyncMock()
    coord._api = api  # type: ignore[assignment]
    entity = PantristPantryAmountNumber(coord, items[0])
    return entity, coord


async def test_native_value_reads_amount(hass: HomeAssistant) -> None:
    entity, _ = _make_entity(hass, amount=4)
    assert entity.native_value == 4.0
    assert entity.unique_id == f"{LIST_ID}_pantry_amount_{ITEM_UUID}"
    # Pantrist's ``amount`` is a package count (dimensionless), not the
    # ``unitId`` of the article content. Don't surface a misleading unit
    # on the Number entity — see number.py for the rationale.
    assert entity.native_unit_of_measurement is None
    assert entity.available is True


async def test_native_value_none_when_item_amount_missing(hass: HomeAssistant) -> None:
    entity, _ = _make_entity(hass, amount=None)
    assert entity.native_value is None


async def test_native_value_handles_non_numeric_amount(hass: HomeAssistant) -> None:
    entity, coord = _make_entity(hass, amount=4)
    # Mutate the coordinator data to a value that can't be cast to float.
    coord.data.pantry["items"][0]["amount"] = "garbage"  # type: ignore[index]
    assert entity.native_value is None


async def test_unavailable_when_item_disappears(hass: HomeAssistant) -> None:
    entity, coord = _make_entity(hass)
    coord.data = PantristData(pantry={"items": []})
    assert entity.available is False
    assert entity.native_value is None


async def test_set_value_sends_delta(hass: HomeAssistant) -> None:
    entity, coord = _make_entity(hass, amount=3)
    await entity.async_set_native_value(5)
    coord.api.change_pantry_item_amount.assert_awaited_once_with(
        LIST_ID, item_id=ITEM_UUID, change=2.0, unit_id="kg"
    )


async def test_set_value_noop_when_unchanged(hass: HomeAssistant) -> None:
    entity, coord = _make_entity(hass, amount=3)
    await entity.async_set_native_value(3)
    coord.api.change_pantry_item_amount.assert_not_awaited()


async def test_set_value_raises_when_item_gone(hass: HomeAssistant) -> None:
    entity, coord = _make_entity(hass, amount=3)
    coord.data = PantristData(pantry={"items": []})
    with pytest.raises(HomeAssistantError):
        await entity.async_set_native_value(5)


async def test_set_value_translates_auth_error(hass: HomeAssistant) -> None:
    entity, coord = _make_entity(hass, amount=3)
    coord.api.change_pantry_item_amount = AsyncMock(
        side_effect=PantristAuthError("401")
    )
    with pytest.raises(ConfigEntryAuthFailed):
        await entity.async_set_native_value(4)


async def test_set_value_translates_api_error(hass: HomeAssistant) -> None:
    entity, coord = _make_entity(hass, amount=3)
    coord.api.change_pantry_item_amount = AsyncMock(
        side_effect=PantristApiError("503")
    )
    with pytest.raises(HomeAssistantError):
        await entity.async_set_native_value(4)


@pytest.mark.usefixtures("mock_oauth_session", "mock_socketio")
async def test_platform_setup_materialises_initial_items(
    hass: HomeAssistant,
    config_entry: MockConfigEntry,
    mock_api: MagicMock,
) -> None:
    """Initial setup creates one number entity per pantry item."""
    mock_api.get_pantry_list = AsyncMock(
        return_value={
            "listId": LIST_ID,
            "items": [
                {"uuid": ITEM_UUID, "name": "Rice", "amount": 5, "unitId": "kg"},
                {"uuid": "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb", "name": "Salt"},
                # Items with no uuid are skipped — exercises that branch.
                {"name": "Mystery"},
            ],
        }
    )
    config_entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    registry = er.async_get(hass)
    unique_ids = {e.unique_id for e in registry.entities.values()}
    assert f"{LIST_ID}_pantry_amount_{ITEM_UUID}" in unique_ids
    assert (
        f"{LIST_ID}_pantry_amount_bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb"
        in unique_ids
    )


@pytest.mark.usefixtures("mock_oauth_session", "mock_socketio")
async def test_platform_drops_entity_when_item_removed(
    hass: HomeAssistant,
    config_entry: MockConfigEntry,
    mock_api: MagicMock,
) -> None:
    """When pantry contents shift, vanished items get dropped from the registry."""
    from homeassistant.helpers.dispatcher import async_dispatcher_send

    mock_api.get_pantry_list = AsyncMock(
        return_value={
            "listId": LIST_ID,
            "items": [
                {"uuid": ITEM_UUID, "name": "Rice", "amount": 5, "unitId": "kg"},
            ],
        }
    )
    config_entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    registry = er.async_get(hass)
    expected_uid = f"{LIST_ID}_pantry_amount_{ITEM_UUID}"
    assert registry.async_get_entity_id("number", DOMAIN, expected_uid) is not None

    # Mutate the coordinator data to drop the item, then signal.
    coord = config_entry.runtime_data[LIST_ID]
    coord.data = PantristData(pantry={"items": []})
    async_dispatcher_send(
        hass, signal_pantry_items_changed(config_entry.entry_id), LIST_ID
    )
    await hass.async_block_till_done()

    assert registry.async_get_entity_id("number", DOMAIN, expected_uid) is None


@pytest.mark.usefixtures("mock_oauth_session", "mock_socketio")
async def test_platform_adds_entity_for_new_list(
    hass: HomeAssistant,
    config_entry: MockConfigEntry,
    mock_api: MagicMock,
) -> None:
    """signal_new_list spawns entities for the freshly-added list's items."""
    from homeassistant.helpers.dispatcher import async_dispatcher_send

    mock_api.get_pantry_list = AsyncMock(
        return_value={"listId": LIST_ID, "items": []}
    )
    config_entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    # Manually inject a fresh coordinator with one pantry item, mimicking a
    # newly-spawned list, then fire signal_new_list.
    manager = config_entry.runtime_data
    second_list_id = "cccccccc-cccc-4ccc-8ccc-cccccccccccc"
    new_coord = PantristCoordinator(
        hass, config_entry, mock_api, second_list_id, "Second"
    )
    new_coord.data = PantristData(
        pantry={
            "items": [{"uuid": ITEM_UUID, "name": "Flour", "amount": 2}]
        }
    )
    manager._coordinators[second_list_id] = new_coord  # type: ignore[attr-defined]

    async_dispatcher_send(
        hass, signal_new_list(config_entry.entry_id), second_list_id
    )
    await hass.async_block_till_done()

    registry = er.async_get(hass)
    expected_uid = f"{second_list_id}_pantry_amount_{ITEM_UUID}"
    assert registry.async_get_entity_id("number", DOMAIN, expected_uid) is not None
