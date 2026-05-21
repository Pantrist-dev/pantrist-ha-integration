"""Todo entity tests."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest
from homeassistant.components.todo import TodoItem, TodoItemStatus
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed, HomeAssistantError
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.pantrist.api import PantristApiError, PantristAuthError
from custom_components.pantrist.coordinator import PantristCoordinator, PantristData
from custom_components.pantrist.todo import (
    PantristShoppingTodoEntity,
    _describe_item,
)

from .conftest import LIST_ID, LIST_NAME


@pytest.mark.usefixtures("mock_oauth_session", "mock_socketio")
async def test_create_todo_item_calls_add_by_name(
    hass: HomeAssistant,
    config_entry: MockConfigEntry,
    mock_api: MagicMock,
) -> None:
    """User creating a todo item via the Lovelace card adds it to Pantrist."""
    config_entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    coordinator = config_entry.runtime_data[LIST_ID]
    entity = PantristShoppingTodoEntity(coordinator)
    await entity.async_create_todo_item(
        TodoItem(summary="Bananas", status=TodoItemStatus.NEEDS_ACTION)
    )

    mock_api.add_to_shopping_list_by_name.assert_awaited_once_with(LIST_ID, "Bananas")


@pytest.mark.usefixtures("mock_oauth_session", "mock_socketio")
async def test_update_to_completed_calls_check(
    hass: HomeAssistant,
    config_entry: MockConfigEntry,
    mock_api: MagicMock,
) -> None:
    """Ticking the box flips a Pantrist item to the cart via the check endpoint."""
    config_entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    coordinator = config_entry.runtime_data[LIST_ID]
    entity = PantristShoppingTodoEntity(coordinator)
    await entity.async_update_todo_item(
        TodoItem(uid="i1", summary="Milk", status=TodoItemStatus.COMPLETED)
    )
    mock_api.check_shopping_list_item.assert_awaited_once_with(LIST_ID, "i1")


@pytest.mark.usefixtures("mock_oauth_session", "mock_socketio")
async def test_delete_todo_items_calls_delete(
    hass: HomeAssistant,
    config_entry: MockConfigEntry,
    mock_api: MagicMock,
) -> None:
    config_entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    coordinator = config_entry.runtime_data[LIST_ID]
    entity = PantristShoppingTodoEntity(coordinator)
    await entity.async_delete_todo_items(["i1", "i2"])
    assert mock_api.delete_shopping_list_item.await_count == 2


def _make_coordinator(hass: HomeAssistant, data: PantristData) -> PantristCoordinator:
    coord = PantristCoordinator(hass, MagicMock(), MagicMock(), LIST_ID, LIST_NAME)
    coord.data = data
    return coord


async def test_todo_items_projection(hass: HomeAssistant) -> None:
    """todo_items skips entries without uid or summary."""
    coord = _make_coordinator(
        hass,
        PantristData(
            shopping_list={
                "items": [
                    {"uuid": "u1", "name": "Bread", "amount": 1, "unitId": "kg"},
                    {"uuid": None, "name": "no-uid"},
                    {"uuid": "u3", "name": None},
                    {
                        "uuid": "u4",
                        "name": "Eggs",
                        "amount": 6,
                        "brand": "Acme",
                        "notes": "free range",
                    },
                ]
            }
        ),
    )
    entity = PantristShoppingTodoEntity(coord)
    items = entity.todo_items
    assert len(items) == 2
    assert items[0].uid == "u1"
    assert items[0].summary == "Bread"
    assert items[0].description == "1 kg"
    assert items[1].uid == "u4"
    assert items[1].description == "6 · Acme · free range"


async def test_create_todo_rejects_blank_summary(hass: HomeAssistant) -> None:
    """An empty summary surfaces a HomeAssistantError instead of hitting the API."""
    coord = _make_coordinator(hass, PantristData())
    coord._api = MagicMock()
    coord._api.add_to_shopping_list_by_name = AsyncMock()
    entity = PantristShoppingTodoEntity(coord)
    with pytest.raises(HomeAssistantError):
        await entity.async_create_todo_item(
            TodoItem(summary="", status=TodoItemStatus.NEEDS_ACTION)
        )
    coord._api.add_to_shopping_list_by_name.assert_not_awaited()


async def test_create_todo_translates_auth_error(hass: HomeAssistant) -> None:
    """A PantristAuthError surfaces as ConfigEntryAuthFailed."""
    coord = _make_coordinator(hass, PantristData())
    coord._api = MagicMock()
    coord._api.add_to_shopping_list_by_name = AsyncMock(
        side_effect=PantristAuthError("401")
    )
    entity = PantristShoppingTodoEntity(coord)
    with pytest.raises(ConfigEntryAuthFailed):
        await entity.async_create_todo_item(
            TodoItem(summary="X", status=TodoItemStatus.NEEDS_ACTION)
        )


async def test_update_todo_ignores_non_completed(hass: HomeAssistant) -> None:
    """A non-completed update is a no-op."""
    coord = _make_coordinator(hass, PantristData())
    coord._api = MagicMock()
    coord._api.check_shopping_list_item = AsyncMock()
    entity = PantristShoppingTodoEntity(coord)
    await entity.async_update_todo_item(
        TodoItem(uid="u1", summary="x", status=TodoItemStatus.NEEDS_ACTION)
    )
    coord._api.check_shopping_list_item.assert_not_awaited()


async def test_update_todo_translates_auth_error(hass: HomeAssistant) -> None:
    coord = _make_coordinator(hass, PantristData())
    coord._api = MagicMock()
    coord._api.check_shopping_list_item = AsyncMock(
        side_effect=PantristAuthError("401")
    )
    entity = PantristShoppingTodoEntity(coord)
    with pytest.raises(ConfigEntryAuthFailed):
        await entity.async_update_todo_item(
            TodoItem(uid="u1", summary="x", status=TodoItemStatus.COMPLETED)
        )


async def test_delete_todo_translates_auth_error(hass: HomeAssistant) -> None:
    coord = _make_coordinator(hass, PantristData())
    coord._api = MagicMock()
    coord._api.delete_shopping_list_item = AsyncMock(
        side_effect=PantristAuthError("401")
    )
    entity = PantristShoppingTodoEntity(coord)
    with pytest.raises(ConfigEntryAuthFailed):
        await entity.async_delete_todo_items(["u1"])


async def test_create_todo_translates_api_error(hass: HomeAssistant) -> None:
    """Bronze action-exceptions: PantristApiError → HomeAssistantError."""
    coord = _make_coordinator(hass, PantristData())
    coord._api = MagicMock()
    coord._api.add_to_shopping_list_by_name = AsyncMock(
        side_effect=PantristApiError("503")
    )
    entity = PantristShoppingTodoEntity(coord)
    with pytest.raises(HomeAssistantError):
        await entity.async_create_todo_item(
            TodoItem(summary="X", status=TodoItemStatus.NEEDS_ACTION)
        )


async def test_update_todo_translates_api_error(hass: HomeAssistant) -> None:
    coord = _make_coordinator(hass, PantristData())
    coord._api = MagicMock()
    coord._api.check_shopping_list_item = AsyncMock(
        side_effect=PantristApiError("503")
    )
    entity = PantristShoppingTodoEntity(coord)
    with pytest.raises(HomeAssistantError):
        await entity.async_update_todo_item(
            TodoItem(uid="u1", summary="x", status=TodoItemStatus.COMPLETED)
        )


async def test_delete_todo_translates_api_error(hass: HomeAssistant) -> None:
    coord = _make_coordinator(hass, PantristData())
    coord._api = MagicMock()
    coord._api.delete_shopping_list_item = AsyncMock(
        side_effect=PantristApiError("503")
    )
    entity = PantristShoppingTodoEntity(coord)
    with pytest.raises(HomeAssistantError):
        await entity.async_delete_todo_items(["u1"])


def test_describe_item_returns_none_for_empty() -> None:
    """Empty / unknown items get no description string."""
    assert _describe_item({}) is None
