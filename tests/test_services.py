"""Service-call routing tests."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed, HomeAssistantError
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.pantrist import _coordinator_for_call
from custom_components.pantrist.api import PantristApiError, PantristAuthError
from custom_components.pantrist.const import (
    DOMAIN,
    SERVICE_ADD_TO_PANTRY,
    SERVICE_ADD_TO_SHOPPING_LIST,
    SERVICE_ADD_TO_SHOPPING_LIST_BY_BARCODE,
    SERVICE_CHANGE_PANTRY_AMOUNT,
    SERVICE_CHECK_SHOPPING_LIST_ITEM,
    SERVICE_DELETE_PANTRY_ITEM,
    SERVICE_DELETE_SHOPPING_LIST_ITEM,
    SERVICE_SEARCH_PANTRY_ITEMS,
)

from .conftest import LIST_ID


pytestmark = pytest.mark.usefixtures("mock_oauth_session", "mock_socketio")


async def _setup(hass: HomeAssistant, entry: MockConfigEntry) -> MagicMock:
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    return entry.runtime_data[LIST_ID]


async def test_add_to_shopping_list_service(
    hass: HomeAssistant, config_entry: MockConfigEntry, mock_api: MagicMock
) -> None:
    coord = await _setup(hass, config_entry)
    await hass.services.async_call(
        DOMAIN, SERVICE_ADD_TO_SHOPPING_LIST, {"name": "Milk"}, blocking=True
    )
    mock_api.add_to_shopping_list_by_name.assert_awaited_with(LIST_ID, name="Milk")


async def test_add_to_shopping_list_by_barcode_service(
    hass: HomeAssistant, config_entry: MockConfigEntry, mock_api: MagicMock
) -> None:
    await _setup(hass, config_entry)
    await hass.services.async_call(
        DOMAIN,
        SERVICE_ADD_TO_SHOPPING_LIST_BY_BARCODE,
        {"barcode": "1234"},
        blocking=True,
    )
    mock_api.add_to_shopping_list_by_barcode.assert_awaited_with(
        LIST_ID, barcode="1234"
    )


async def test_check_shopping_list_item_service(
    hass: HomeAssistant, config_entry: MockConfigEntry, mock_api: MagicMock
) -> None:
    await _setup(hass, config_entry)
    await hass.services.async_call(
        DOMAIN,
        SERVICE_CHECK_SHOPPING_LIST_ITEM,
        {"item_id": "i1"},
        blocking=True,
    )
    mock_api.check_shopping_list_item.assert_awaited_with(LIST_ID, item_id="i1")


async def test_delete_shopping_list_item_service(
    hass: HomeAssistant, config_entry: MockConfigEntry, mock_api: MagicMock
) -> None:
    await _setup(hass, config_entry)
    await hass.services.async_call(
        DOMAIN,
        SERVICE_DELETE_SHOPPING_LIST_ITEM,
        {"item_id": "i1"},
        blocking=True,
    )
    mock_api.delete_shopping_list_item.assert_awaited_with(LIST_ID, item_id="i1")


async def test_add_to_pantry_service(
    hass: HomeAssistant, config_entry: MockConfigEntry, mock_api: MagicMock
) -> None:
    await _setup(hass, config_entry)
    await hass.services.async_call(
        DOMAIN,
        SERVICE_ADD_TO_PANTRY,
        {"name": "Rice", "amount": 2, "unit_id": "kg"},
        blocking=True,
    )
    mock_api.add_to_pantry_by_name.assert_awaited_with(
        LIST_ID, name="Rice", amount=2.0, unit_id="kg"
    )


async def test_delete_pantry_item_service(
    hass: HomeAssistant, config_entry: MockConfigEntry, mock_api: MagicMock
) -> None:
    await _setup(hass, config_entry)
    await hass.services.async_call(
        DOMAIN,
        SERVICE_DELETE_PANTRY_ITEM,
        {"item_id": "p1"},
        blocking=True,
    )
    mock_api.delete_pantry_item.assert_awaited_with(LIST_ID, item_id="p1")


async def test_change_pantry_amount_service(
    hass: HomeAssistant, config_entry: MockConfigEntry, mock_api: MagicMock
) -> None:
    await _setup(hass, config_entry)
    await hass.services.async_call(
        DOMAIN,
        SERVICE_CHANGE_PANTRY_AMOUNT,
        {"item_id": "p1", "change": -1.5},
        blocking=True,
    )
    # auto_restock defaults to True on the HA service so NFC / voice
    # automations get "consume + reorder" out of the box.
    mock_api.change_pantry_item_amount.assert_awaited_with(
        LIST_ID, item_id="p1", change=-1.5, auto_restock=True
    )

    # Auto-restock can be turned off explicitly.
    mock_api.change_pantry_item_amount.reset_mock()
    await hass.services.async_call(
        DOMAIN,
        SERVICE_CHANGE_PANTRY_AMOUNT,
        {"item_id": "p1", "change": -1.5, "auto_restock": False},
        blocking=True,
    )
    mock_api.change_pantry_item_amount.assert_awaited_with(
        LIST_ID, item_id="p1", change=-1.5, auto_restock=False
    )


def _seed_pantry(mock_api: MagicMock, items: list[dict]) -> None:
    """Point the coordinator's pantry fetch at a fixed item set."""
    mock_api.get_pantry_list.return_value = {"listId": LIST_ID, "items": items}


async def test_change_pantry_amount_by_name(
    hass: HomeAssistant, config_entry: MockConfigEntry, mock_api: MagicMock
) -> None:
    """A name is resolved to its UUID against the live pantry (case-insensitive)."""
    _seed_pantry(
        mock_api,
        [
            {"uuid": "milk-uuid", "name": "Milk"},
            {"uuid": "eggs-uuid", "name": "Eggs"},
        ],
    )
    await _setup(hass, config_entry)
    await hass.services.async_call(
        DOMAIN,
        SERVICE_CHANGE_PANTRY_AMOUNT,
        {"name": "milk", "change": -1},
        blocking=True,
    )
    mock_api.change_pantry_item_amount.assert_awaited_with(
        LIST_ID, item_id="milk-uuid", change=-1.0, auto_restock=True
    )


async def test_change_pantry_amount_name_not_found(
    hass: HomeAssistant, config_entry: MockConfigEntry, mock_api: MagicMock
) -> None:
    _seed_pantry(mock_api, [{"uuid": "milk-uuid", "name": "Milk"}])
    await _setup(hass, config_entry)
    with pytest.raises(HomeAssistantError):
        await hass.services.async_call(
            DOMAIN,
            SERVICE_CHANGE_PANTRY_AMOUNT,
            {"name": "Sugar", "change": -1},
            blocking=True,
        )
    mock_api.change_pantry_item_amount.assert_not_awaited()


async def test_change_pantry_amount_ambiguous_name(
    hass: HomeAssistant, config_entry: MockConfigEntry, mock_api: MagicMock
) -> None:
    """A substring that matches several items forces a UUID disambiguation."""
    _seed_pantry(
        mock_api,
        [
            {"uuid": "whole-uuid", "name": "Whole Milk"},
            {"uuid": "oat-uuid", "name": "Oat Milk"},
        ],
    )
    await _setup(hass, config_entry)
    with pytest.raises(HomeAssistantError):
        await hass.services.async_call(
            DOMAIN,
            SERVICE_CHANGE_PANTRY_AMOUNT,
            {"name": "milk", "change": -1},
            blocking=True,
        )
    mock_api.change_pantry_item_amount.assert_not_awaited()


async def test_change_pantry_amount_requires_identifier(
    hass: HomeAssistant, config_entry: MockConfigEntry, mock_api: MagicMock
) -> None:
    await _setup(hass, config_entry)
    with pytest.raises(HomeAssistantError):
        await hass.services.async_call(
            DOMAIN,
            SERVICE_CHANGE_PANTRY_AMOUNT,
            {"change": -1},
            blocking=True,
        )
    mock_api.change_pantry_item_amount.assert_not_awaited()


async def test_search_pantry_items_with_query(
    hass: HomeAssistant, config_entry: MockConfigEntry, mock_api: MagicMock
) -> None:
    """The search action returns matching items with their UUIDs."""
    _seed_pantry(
        mock_api,
        [
            {
                "uuid": "milk-uuid",
                "name": "Milk",
                "amount": 2,
                "contentVolume": 1.5,
                "unitId": "L",
                "brand": "Acme",
            },
            {"uuid": "eggs-uuid", "name": "Eggs", "amount": 6},
        ],
    )
    await _setup(hass, config_entry)
    response = await hass.services.async_call(
        DOMAIN,
        SERVICE_SEARCH_PANTRY_ITEMS,
        {"query": "milk"},
        blocking=True,
        return_response=True,
    )
    assert response == {
        "list_id": LIST_ID,
        "items": [
            {
                "item_id": "milk-uuid",
                "name": "Milk",
                "amount": 2,
                "content_volume": 1.5,
                "unit": "L",
                "brand": "Acme",
            }
        ],
    }


async def test_search_pantry_items_without_query_returns_all(
    hass: HomeAssistant, config_entry: MockConfigEntry, mock_api: MagicMock
) -> None:
    _seed_pantry(
        mock_api,
        [
            {"uuid": "milk-uuid", "name": "Milk"},
            {"uuid": "eggs-uuid", "name": "Eggs"},
        ],
    )
    await _setup(hass, config_entry)
    response = await hass.services.async_call(
        DOMAIN,
        SERVICE_SEARCH_PANTRY_ITEMS,
        {},
        blocking=True,
        return_response=True,
    )
    assert [i["item_id"] for i in response["items"]] == ["milk-uuid", "eggs-uuid"]


async def test_service_with_explicit_list_id(
    hass: HomeAssistant, config_entry: MockConfigEntry, mock_api: MagicMock
) -> None:
    """Explicit list_id is honoured (still resolves to the configured coordinator)."""
    await _setup(hass, config_entry)
    await hass.services.async_call(
        DOMAIN,
        SERVICE_ADD_TO_SHOPPING_LIST,
        {"name": "Bread", "list_id": LIST_ID},
        blocking=True,
    )
    mock_api.add_to_shopping_list_by_name.assert_awaited_with(LIST_ID, name="Bread")


async def test_service_unknown_list_id_raises(
    hass: HomeAssistant, config_entry: MockConfigEntry, mock_api: MagicMock
) -> None:
    """Passing a list_id we don't manage surfaces a HomeAssistantError."""
    await _setup(hass, config_entry)
    with pytest.raises(HomeAssistantError):
        await hass.services.async_call(
            DOMAIN,
            SERVICE_ADD_TO_SHOPPING_LIST,
            {"name": "X", "list_id": "ffffffff-ffff-4fff-8fff-ffffffffffff"},
            blocking=True,
        )


async def test_service_auth_error_translates_to_reauth(
    hass: HomeAssistant, config_entry: MockConfigEntry, mock_api: MagicMock
) -> None:
    """A PantristAuthError surfaces as ConfigEntryAuthFailed."""
    mock_api.add_to_shopping_list_by_name = AsyncMock(
        side_effect=PantristAuthError("401")
    )
    await _setup(hass, config_entry)
    with pytest.raises(ConfigEntryAuthFailed):
        await hass.services.async_call(
            DOMAIN, SERVICE_ADD_TO_SHOPPING_LIST, {"name": "X"}, blocking=True
        )


async def test_service_api_error_translates_to_home_assistant_error(
    hass: HomeAssistant, config_entry: MockConfigEntry, mock_api: MagicMock
) -> None:
    """Bronze action-exceptions: PantristApiError must not leak as itself."""
    mock_api.add_to_shopping_list_by_name = AsyncMock(
        side_effect=PantristApiError("503 service unavailable")
    )
    await _setup(hass, config_entry)
    with pytest.raises(HomeAssistantError) as excinfo:
        await hass.services.async_call(
            DOMAIN, SERVICE_ADD_TO_SHOPPING_LIST, {"name": "X"}, blocking=True
        )
    # The wrapped exception preserves the original message.
    assert "503" in str(excinfo.value)


def test_coordinator_for_call_without_entries(hass: HomeAssistant) -> None:
    """No configured entry → HomeAssistantError."""
    with pytest.raises(HomeAssistantError):
        _coordinator_for_call(hass, None)


async def test_async_setup_registers_services_before_entry(
    hass: HomeAssistant,
) -> None:
    """Bronze action-setup: services must be registered in async_setup,
    so YAML automations can resolve them before any entry is configured.
    """
    from homeassistant.setup import async_setup_component

    # ``async_setup_component`` resolves the ``application_credentials``
    # dependency declared in ``manifest.json`` before invoking our
    # ``async_setup``. Calling the latter directly would crash on the
    # ``async_import_client_credential`` call because the platform isn't
    # loaded yet.
    assert await async_setup_component(hass, DOMAIN, {})
    assert hass.services.has_service(DOMAIN, SERVICE_ADD_TO_SHOPPING_LIST)
    # Calling it without a config entry must raise a clean HA error,
    # not crash the service registry.
    with pytest.raises(HomeAssistantError):
        await hass.services.async_call(
            DOMAIN, SERVICE_ADD_TO_SHOPPING_LIST, {"name": "X"}, blocking=True
        )
