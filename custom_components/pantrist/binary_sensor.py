"""Pantrist binary sensors.

Three per Pantrist list, each driven straight off the coordinator snapshot:

  * ``low_stock``         — any pantry item is at or below its minimum amount
  * ``has_expired_items`` — any pantry item is past its earliest best-before
  * ``shopping_list_has_items`` — the active shopping list is non-empty
"""

from __future__ import annotations

from datetime import date, datetime
import logging

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .coordinator import PantristCoordinator
from .entity import PantristEntity
from .list_manager import PantristListManager, signal_new_list

_LOGGER = logging.getLogger(__name__)

PARALLEL_UPDATES = 0


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add three binary sensors per Pantrist list (dynamic)."""
    manager: PantristListManager = entry.runtime_data

    @callback
    def _build(coordinator: PantristCoordinator) -> list[BinarySensorEntity]:
        return [
            PantristLowStockBinarySensor(coordinator),
            PantristHasExpiredBinarySensor(coordinator),
            PantristShoppingListHasItemsBinarySensor(coordinator),
        ]

    initial: list[BinarySensorEntity] = []
    for coordinator in manager.values():
        initial.extend(_build(coordinator))
    async_add_entities(initial)

    @callback
    def _on_new_list(list_id: str) -> None:
        async_add_entities(_build(manager[list_id]))

    entry.async_on_unload(
        async_dispatcher_connect(
            hass, signal_new_list(entry.entry_id), _on_new_list
        )
    )


class _PantristBinarySensorBase(PantristEntity, BinarySensorEntity):
    """Base for Pantrist binary sensors keyed on the coordinator's snapshot."""

    def __init__(self, coordinator: PantristCoordinator, key: str) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.list_id}_{key}"


class PantristLowStockBinarySensor(_PantristBinarySensorBase):
    """ON when any tracked pantry item has fallen at or below its minimum."""

    _attr_icon = "mdi:alert-decagram"
    _attr_translation_key = "low_stock"
    _attr_device_class = BinarySensorDeviceClass.PROBLEM

    def __init__(self, coordinator: PantristCoordinator) -> None:
        super().__init__(coordinator, "low_stock")

    @property
    def is_on(self) -> bool:
        items = (self.coordinator.data.pantry or {}).get("items", [])
        return any(
            item.get("manageMinimumAmount")
            and item.get("amount", 0) <= item.get("minimumAmount", 0)
            for item in items
        )


class PantristHasExpiredBinarySensor(_PantristBinarySensorBase):
    """ON when any pantry item is past its earliest best-before date."""

    _attr_icon = "mdi:food-off"
    _attr_translation_key = "has_expired_items"
    _attr_device_class = BinarySensorDeviceClass.PROBLEM

    def __init__(self, coordinator: PantristCoordinator) -> None:
        super().__init__(coordinator, "has_expired_items")

    @property
    def is_on(self) -> bool:
        today = date.today()
        items = (self.coordinator.data.pantry or {}).get("items", [])
        for item in items:
            earliest = (item.get("pantrySettings") or {}).get("earliestBestBefore")
            if not earliest:
                continue
            try:
                bb = datetime.strptime(earliest, "%d-%m-%Y").date()
            except (ValueError, TypeError):
                continue
            if bb < today:
                return True
        return False


class PantristShoppingListHasItemsBinarySensor(_PantristBinarySensorBase):
    """ON when the shopping list has at least one outstanding item."""

    _attr_icon = "mdi:cart-arrow-down"
    _attr_translation_key = "shopping_list_has_items"
    # No device_class — "has items" isn't a problem state, just a flag.

    def __init__(self, coordinator: PantristCoordinator) -> None:
        super().__init__(coordinator, "shopping_list_has_items")

    @property
    def is_on(self) -> bool:
        items = (self.coordinator.data.shopping_list or {}).get("items", [])
        return len(items) > 0
