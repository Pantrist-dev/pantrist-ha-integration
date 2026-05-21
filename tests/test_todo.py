"""Todo entity tests."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest
from homeassistant.components.todo import TodoItem, TodoItemStatus
from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.pantrist.const import DOMAIN

from .conftest import LIST_ID


@pytest.mark.usefixtures("enable_custom_integrations", "setup_credentials", "mock_socketio")
async def test_create_todo_item_calls_add_by_name(
    hass: HomeAssistant,
    config_entry: MockConfigEntry,
    mock_api: MagicMock,
) -> None:
    """User creating a todo item via the Lovelace card adds it to Pantrist."""
    config_entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    coordinators = hass.data[DOMAIN][config_entry.entry_id]
    coordinator = coordinators[LIST_ID]

    # Reach into the todo entity (HA platform owns the registry).
    from custom_components.pantrist.todo import PantristShoppingTodoEntity

    entity = PantristShoppingTodoEntity(coordinator)
    await entity.async_create_todo_item(
        TodoItem(summary="Bananas", status=TodoItemStatus.NEEDS_ACTION)
    )

    mock_api.add_to_shopping_list_by_name.assert_awaited_once_with(LIST_ID, "Bananas")


@pytest.mark.usefixtures("enable_custom_integrations", "setup_credentials", "mock_socketio")
async def test_update_to_completed_calls_check(
    hass: HomeAssistant,
    config_entry: MockConfigEntry,
    mock_api: MagicMock,
) -> None:
    """Ticking the box flips a Pantrist item to the cart via the check endpoint."""
    config_entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    coordinator = hass.data[DOMAIN][config_entry.entry_id][LIST_ID]

    from custom_components.pantrist.todo import PantristShoppingTodoEntity

    entity = PantristShoppingTodoEntity(coordinator)
    await entity.async_update_todo_item(
        TodoItem(uid="i1", summary="Milk", status=TodoItemStatus.COMPLETED)
    )
    mock_api.check_shopping_list_item.assert_awaited_once_with(LIST_ID, "i1")


@pytest.mark.usefixtures("enable_custom_integrations", "setup_credentials", "mock_socketio")
async def test_delete_todo_items_calls_delete(
    hass: HomeAssistant,
    config_entry: MockConfigEntry,
    mock_api: MagicMock,
) -> None:
    config_entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    coordinator = hass.data[DOMAIN][config_entry.entry_id][LIST_ID]

    from custom_components.pantrist.todo import PantristShoppingTodoEntity

    entity = PantristShoppingTodoEntity(coordinator)
    await entity.async_delete_todo_items(["i1", "i2"])
    assert mock_api.delete_shopping_list_item.await_count == 2
