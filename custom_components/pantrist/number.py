"""Pantrist pantry-amount number entities.

One ``number.<list>_<item>_amount`` entity per pantry item, so users can
adjust a stockpile from the HA dashboard the same way the Pantrist mobile
app lets them. The new value is sent to Pantrist via
``api.change_pantry_item_amount`` as a delta (current → target), and the
coordinator's Socket.IO subscription reflects the change back on the
next ``data:updated`` event.

The set of entities is *dynamic*: each list's coordinator publishes
``signal_pantry_items_changed`` whenever the pantry contents shift, and
this platform reconciles its entities against the new item set —
spawning fresh entities for items that have been added and dropping the
HA registry entries for items that have been removed.
"""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import ConfigEntryAuthFailed, HomeAssistantError
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .api import PantristApiError, PantristAuthError
from .const import DOMAIN
from .coordinator import PantristCoordinator
from .entity import PantristEntity
from .list_manager import (
    PantristListManager,
    signal_new_list,
    signal_pantry_items_changed,
)

_LOGGER = logging.getLogger(__name__)

PARALLEL_UPDATES = 1


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Initial entities + dispatcher subscriptions for dynamic items + lists."""
    manager: PantristListManager = entry.runtime_data
    known: dict[str, set[str]] = {}  # list_id → {item_uuid}

    @callback
    def _add_for_list(coordinator: PantristCoordinator) -> None:
        """Materialise any pantry items in ``coordinator`` not yet known."""
        seen = known.setdefault(coordinator.list_id, set())
        items = (coordinator.data.pantry or {}).get("items", [])
        new_entities: list[NumberEntity] = []
        seen_now: set[str] = set()
        for item in items:
            uuid = item.get("uuid")
            if not uuid:
                continue
            seen_now.add(uuid)
            if uuid in seen:
                continue
            seen.add(uuid)
            new_entities.append(PantristPantryAmountNumber(coordinator, item))

        # Items that were here last time but are gone now → drop the
        # entity-registry rows so the HA UI doesn't keep stale placeholders.
        gone = seen - seen_now
        if gone:
            seen.difference_update(gone)
            registry = er.async_get(hass)
            for uuid in gone:
                unique_id = _amount_unique_id(coordinator.list_id, uuid)
                entry_obj = registry.async_get_entity_id(
                    "number", DOMAIN, unique_id
                )
                if entry_obj is not None:
                    registry.async_remove(entry_obj)

        if new_entities:
            async_add_entities(new_entities)

    # Initial sweep across every list.
    for coordinator in manager.values():
        _add_for_list(coordinator)

    @callback
    def _on_new_list(list_id: str) -> None:
        _add_for_list(manager[list_id])

    @callback
    def _on_items_changed(list_id: str) -> None:
        coord = manager.coordinators.get(list_id)
        if coord is not None:
            _add_for_list(coord)

    entry.async_on_unload(
        async_dispatcher_connect(
            hass, signal_new_list(entry.entry_id), _on_new_list
        )
    )
    entry.async_on_unload(
        async_dispatcher_connect(
            hass,
            signal_pantry_items_changed(entry.entry_id),
            _on_items_changed,
        )
    )


def _amount_unique_id(list_id: str, item_uuid: str) -> str:
    return f"{list_id}_pantry_amount_{item_uuid}"


class PantristPantryAmountNumber(PantristEntity, NumberEntity):
    """Per-pantry-item amount slider."""

    _attr_translation_key = "pantry_amount"
    _attr_mode = NumberMode.BOX
    _attr_native_min_value = 0
    _attr_native_max_value = 9999
    _attr_native_step = 0.1
    _attr_icon = "mdi:tray-full"

    def __init__(
        self, coordinator: PantristCoordinator, item: dict[str, Any]
    ) -> None:
        super().__init__(coordinator)
        self._item_uuid = str(item.get("uuid") or "")
        # Friendly entity name = item name; falls back to a UUID stub so we
        # never end up with blank UI rows when the API gives us a half-baked
        # payload.
        item_name = item.get("name") or f"Item {self._item_uuid[:8]}…"
        self._attr_translation_placeholders = {"item": str(item_name)}
        self._attr_name = str(item_name)
        self._attr_unique_id = _amount_unique_id(
            coordinator.list_id, self._item_uuid
        )
        self._attr_native_unit_of_measurement = item.get("unitId")

    @property
    def _item(self) -> dict[str, Any] | None:
        """Find this entity's item in the current coordinator snapshot."""
        items = (self.coordinator.data.pantry or {}).get("items", [])
        for raw in items:
            if raw.get("uuid") == self._item_uuid:
                return dict(raw)
        return None

    @property
    def available(self) -> bool:
        return (
            super().available
            and self._item is not None
        )

    @property
    def native_value(self) -> float | None:
        item = self._item
        if item is None:
            return None
        amount = item.get("amount")
        if amount is None:
            return None
        try:
            return float(amount)
        except (TypeError, ValueError):
            return None

    async def async_set_native_value(self, value: float) -> None:
        item = self._item
        if item is None:
            # The item evaporated under us — surface as a clean HA error.
            raise HomeAssistantError(
                translation_domain=DOMAIN,
                translation_key="number_set_failed",
                translation_placeholders={
                    "name": self._attr_name or self._item_uuid,
                    "error": "item no longer in pantry",
                },
            )
        current = float(item.get("amount") or 0)
        change = value - current
        if change == 0:
            return
        try:
            await self.coordinator.api.change_pantry_item_amount(
                self.coordinator.list_id,
                item_id=self._item_uuid,
                change=change,
                unit_id=item.get("unitId"),
            )
        except PantristAuthError as err:
            raise ConfigEntryAuthFailed("Pantrist auth failed") from err
        except PantristApiError as err:
            raise HomeAssistantError(
                translation_domain=DOMAIN,
                translation_key="number_set_failed",
                translation_placeholders={
                    "name": self._attr_name or self._item_uuid,
                    "error": str(err),
                },
            ) from err
        await self.coordinator.async_request_refresh()
