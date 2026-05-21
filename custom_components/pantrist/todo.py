"""Pantrist todo-list entities.

Each Pantrist list exposes one ``todo.<list>_shopping_list`` entity. The
shopping list maps cleanly to HA's TodoListEntity contract:

  * `async_create_todo_item` → `pantrist.add_to_shopping_list_by_name`
  * `async_update_todo_item` (status = COMPLETED) → `check_shopping_list_item`
    (Pantrist's "check" moves the item to the shopping cart, so the entry
    disappears from the active shopping list on the next refresh — which is
    semantically what HA's "completed" status means.)
  * `async_delete_todo_items` → `delete_shopping_list_item` per uid
"""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.todo import (
    TodoItem,
    TodoItemStatus,
    TodoListEntity,
    TodoListEntityFeature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed, HomeAssistantError
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .api import PantristApiError, PantristAuthError
from .const import DOMAIN
from .coordinator import PantristCoordinator
from .entity import PantristEntity

_LOGGER = logging.getLogger(__name__)

# Pantrist's REST endpoints serialize per-list writes; serialise per-entity
# here too to avoid the Lovelace todo card racing add/check/delete calls.
PARALLEL_UPDATES = 1


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Create one shopping-list todo entity per Pantrist list."""
    coordinators: dict[str, PantristCoordinator] = entry.runtime_data
    async_add_entities(
        PantristShoppingTodoEntity(coordinator)
        for coordinator in coordinators.values()
    )


class PantristShoppingTodoEntity(PantristEntity, TodoListEntity):
    """Active shopping list as an HA todo entity."""

    _attr_icon = "mdi:cart"
    _attr_translation_key = "shopping_list_todo"
    _attr_supported_features = (
        TodoListEntityFeature.CREATE_TODO_ITEM
        | TodoListEntityFeature.UPDATE_TODO_ITEM
        | TodoListEntityFeature.DELETE_TODO_ITEM
    )

    def __init__(self, coordinator: PantristCoordinator) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.list_id}_shopping_list_todo"

    @property
    def todo_items(self) -> list[TodoItem]:
        """Items currently on the shopping list — all NEEDS_ACTION.

        Checked items disappear from the shopping list (Pantrist moves them
        to the cart), so the only items we ever return here are pending.
        """
        items = (self.coordinator.data.shopping_list or {}).get("items", [])
        out: list[TodoItem] = []
        for raw in items:
            uid = raw.get("uuid")
            summary = raw.get("name")
            if not uid or not summary:
                continue
            description = _describe_item(raw)
            out.append(
                TodoItem(
                    uid=uid,
                    summary=summary,
                    status=TodoItemStatus.NEEDS_ACTION,
                    description=description,
                )
            )
        return out

    async def async_create_todo_item(self, item: TodoItem) -> None:
        """User clicked + Add in the Lovelace todo card."""
        if not item.summary:
            raise HomeAssistantError("Shopping-list item needs a name")
        try:
            await self.coordinator.api.add_to_shopping_list_by_name(
                self.coordinator.list_id, item.summary
            )
        except PantristAuthError as err:
            raise ConfigEntryAuthFailed("Pantrist auth failed") from err
        except PantristApiError as err:
            raise HomeAssistantError(
                f"Could not add shopping-list item: {err}"
            ) from err
        await self.coordinator.async_request_refresh()

    async def async_update_todo_item(self, item: TodoItem) -> None:
        """User checked the box in the Lovelace todo card.

        We only act on status transitions to COMPLETED — Pantrist doesn't
        support renaming via this endpoint and there's no uncheck (checked
        items have already moved to the cart by the time HA sends us
        anything).
        """
        if item.status != TodoItemStatus.COMPLETED or not item.uid:
            return
        try:
            await self.coordinator.api.check_shopping_list_item(
                self.coordinator.list_id, item.uid
            )
        except PantristAuthError as err:
            raise ConfigEntryAuthFailed("Pantrist auth failed") from err
        except PantristApiError as err:
            raise HomeAssistantError(
                f"Could not check shopping-list item: {err}"
            ) from err
        await self.coordinator.async_request_refresh()

    async def async_delete_todo_items(self, uids: list[str]) -> None:
        for uid in uids:
            try:
                await self.coordinator.api.delete_shopping_list_item(
                    self.coordinator.list_id, uid
                )
            except PantristAuthError as err:
                raise ConfigEntryAuthFailed("Pantrist auth failed") from err
            except PantristApiError as err:
                raise HomeAssistantError(
                    f"Could not delete shopping-list item {uid}: {err}"
                ) from err
        await self.coordinator.async_request_refresh()


def _describe_item(raw: dict[str, Any]) -> str | None:
    """Compact one-liner with amount/unit/brand/notes for the todo description."""
    parts: list[str] = []
    amount = raw.get("amount")
    unit = raw.get("unitId")
    if amount is not None:
        parts.append(f"{amount}{(' ' + unit) if unit else ''}")
    brand = raw.get("brand")
    if brand:
        parts.append(str(brand))
    notes = raw.get("notes")
    if notes:
        parts.append(str(notes))
    return " · ".join(parts) if parts else None
