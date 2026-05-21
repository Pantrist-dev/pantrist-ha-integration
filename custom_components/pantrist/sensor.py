"""Pantrist sensor entities."""

from __future__ import annotations

from datetime import date, datetime, timedelta
import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    DOMAIN,
    SENSOR_EXPIRING_SOON,
    SENSOR_PANTRY,
    SENSOR_SHOPPING_CART,
    SENSOR_SHOPPING_LIST,
)
from .coordinator import PantristCoordinator, PantristData
from .entity import PantristEntity

_LOGGER = logging.getLogger(__name__)

# Coordinator-backed read-only sensors — no per-entity API traffic.
PARALLEL_UPDATES = 0

EXPIRY_WARNING_DAYS_DEFAULT = 7


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add 4 sensors per Pantrist list under this entry."""
    coordinators: dict[str, PantristCoordinator] = entry.runtime_data
    entities: list[SensorEntity] = []
    for coordinator in coordinators.values():
        entities.extend(
            [
                PantristShoppingListSensor(coordinator),
                PantristPantrySensor(coordinator),
                PantristExpiringSoonSensor(coordinator),
                PantristShoppingCartSensor(coordinator),
            ]
        )
    async_add_entities(entities)


def _format_item(item: dict[str, Any]) -> dict[str, Any]:
    """Extract a concise ArticleDto projection for HA attributes."""
    return {
        "uuid": item.get("uuid"),
        "name": item.get("name", ""),
        "amount": item.get("amount"),
        "unit": item.get("unitId"),
        "brand": item.get("brand"),
        "category_uuid": item.get("categoryUuid"),
        "notes": item.get("notes"),
        "image_url": item.get("imageUrl"),
    }


class _PantristBaseSensor(PantristEntity, SensorEntity):
    """Common base for Pantrist sensors tied to one list."""

    _attr_native_unit_of_measurement = "items"

    def __init__(self, coordinator: PantristCoordinator, key: str) -> None:
        super().__init__(coordinator)
        self._key = key
        self._attr_unique_id = f"{coordinator.list_id}_{key}"

    @property
    def data(self) -> PantristData:
        return self.coordinator.data


class PantristShoppingListSensor(_PantristBaseSensor):
    """Number of items on the shopping list + per-item attributes."""

    _attr_icon = "mdi:cart"
    _attr_translation_key = "shopping_list"

    def __init__(self, coordinator: PantristCoordinator) -> None:
        super().__init__(coordinator, SENSOR_SHOPPING_LIST)

    @property
    def native_value(self) -> int:
        return len(self.data.shopping_list.get("items", []))

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        items = self.data.shopping_list.get("items", [])
        return {
            "list_id": self.coordinator.list_id,
            "items": [_format_item(i) for i in items],
        }


class PantristPantrySensor(_PantristBaseSensor):
    """Pantry item count + low-stock attributes."""

    _attr_icon = "mdi:fridge"
    _attr_translation_key = "pantry"

    def __init__(self, coordinator: PantristCoordinator) -> None:
        super().__init__(coordinator, SENSOR_PANTRY)

    @property
    def native_value(self) -> int:
        return len(self.data.pantry.get("items", []))

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        items = self.data.pantry.get("items", [])
        low_stock = [
            _format_item(i)
            for i in items
            if i.get("manageMinimumAmount")
            and i.get("amount", 0) <= i.get("minimumAmount", 0)
        ]
        return {
            "list_id": self.coordinator.list_id,
            "items": [_format_item(i) for i in items],
            "low_stock_count": len(low_stock),
            "low_stock_items": low_stock,
        }


class PantristExpiringSoonSensor(_PantristBaseSensor):
    """Number of pantry items expiring within the warning window."""

    _attr_icon = "mdi:calendar-alert"
    _attr_translation_key = "expiring_soon"

    def __init__(self, coordinator: PantristCoordinator) -> None:
        super().__init__(coordinator, SENSOR_EXPIRING_SOON)

    def _split_expiring(self) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        items = self.data.pantry.get("items", [])
        today = date.today()
        cutoff = today + timedelta(days=EXPIRY_WARNING_DAYS_DEFAULT)

        expiring: list[dict[str, Any]] = []
        expired: list[dict[str, Any]] = []

        for item in items:
            settings = item.get("pantrySettings") or {}
            earliest = settings.get("earliestBestBefore")
            if not earliest:
                continue
            try:
                bb = datetime.strptime(earliest, "%d-%m-%Y").date()
            except (ValueError, TypeError):
                continue
            formatted = {**_format_item(item), "best_before": earliest}
            if bb < today:
                expired.append(formatted)
            elif bb <= cutoff:
                expiring.append(formatted)

        expiring.sort(key=lambda x: x["best_before"])
        expired.sort(key=lambda x: x["best_before"])
        return expiring, expired

    @property
    def native_value(self) -> int:
        expiring, expired = self._split_expiring()
        return len(expiring) + len(expired)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        expiring, expired = self._split_expiring()
        return {
            "list_id": self.coordinator.list_id,
            "warning_days": EXPIRY_WARNING_DAYS_DEFAULT,
            "expiring_count": len(expiring),
            "expired_count": len(expired),
            "expiring_items": expiring,
            "expired_items": expired,
        }


class PantristShoppingCartSensor(_PantristBaseSensor):
    """Items currently in the intermediate shopping cart."""

    _attr_icon = "mdi:cart-check"
    _attr_translation_key = "shopping_cart"

    def __init__(self, coordinator: PantristCoordinator) -> None:
        super().__init__(coordinator, SENSOR_SHOPPING_CART)

    @property
    def native_value(self) -> int:
        return len(self.data.shopping_cart)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        items = self.data.shopping_cart
        return {
            "list_id": self.coordinator.list_id,
            "items": [
                {
                    "cart_uuid": i.get("uuid"),
                    "moved_at": i.get("movedAt"),
                    **_format_item(i.get("article") or {}),
                }
                for i in items
            ],
        }
