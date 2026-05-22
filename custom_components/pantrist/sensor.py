"""Pantrist sensor entities."""

from __future__ import annotations

from datetime import date, datetime, time, timedelta, timezone
import logging
from typing import Any

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    DOMAIN,
    SENSOR_EXPIRING_SOON,
    SENSOR_LATEST_SHOPPING_ITEM,
    SENSOR_NEXT_EXPIRATION,
    SENSOR_PANTRY,
    SENSOR_SHOPPING_CART,
    SENSOR_SHOPPING_LIST,
)
from .coordinator import PantristCoordinator, PantristData
from .entity import PantristEntity
from .list_manager import PantristListManager, signal_new_list

_LOGGER = logging.getLogger(__name__)

# Coordinator-backed read-only sensors — no per-entity API traffic.
PARALLEL_UPDATES = 0

EXPIRY_WARNING_DAYS_DEFAULT = 7


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add sensors per Pantrist list, now and as new lists appear."""
    manager: PantristListManager = entry.runtime_data

    @callback
    def _build(coordinator: PantristCoordinator) -> list[SensorEntity]:
        return [
            PantristShoppingListSensor(coordinator),
            PantristPantrySensor(coordinator),
            PantristExpiringSoonSensor(coordinator),
            PantristShoppingCartSensor(coordinator),
            PantristNextExpirationSensor(coordinator),
            PantristLatestShoppingItemSensor(coordinator),
        ]

    initial: list[SensorEntity] = []
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


def _format_item(item: dict[str, Any]) -> dict[str, Any]:
    """Extract a concise ArticleDto projection for HA attributes.

    Pantrist's data model splits an article's quantity into three pieces:

      * ``amount`` — how many *packages* of the article (dimensionless).
      * ``content_volume`` — how much *content* is in each package
        (dimensioned by ``unit``).
      * ``unit`` — the unit of the content, e.g. ``L`` for milk cartons.

    Exposing all three lets dashboards render "3 × 1 L" rather than the
    nonsensical "3 L" you'd get if ``amount`` and ``unit`` were paired
    directly. The pre-composed ``display`` field is provided as a
    convenience for ``markdown`` cards.
    """
    amount = item.get("amount")
    content_volume = item.get("contentVolume")
    unit = item.get("unitId")
    return {
        "uuid": item.get("uuid"),
        "name": item.get("name", ""),
        "amount": amount,
        "content_volume": content_volume,
        "unit": unit,
        "display": _compose_display(amount, content_volume, unit),
        "brand": item.get("brand"),
        "category_uuid": item.get("categoryUuid"),
        "notes": item.get("notes"),
        "image_url": item.get("imageUrl"),
    }


def _compose_display(
    amount: Any, content_volume: Any, unit: str | None
) -> str | None:
    """Render the canonical "<n> × <v> <unit>" string for an item.

    ``amount=3, content_volume=1, unit="L"`` → ``"3 × 1 L"``.
    Falls back gracefully when content_volume or unit is missing:
    ``amount=3, content_volume=None`` → ``"3"``;
    ``amount=3, content_volume=1.5, unit=None`` → ``"3 × 1.5"``.
    Returns None if no quantity info is set at all.
    """
    if amount is None:
        return None
    out = _fmt_num(amount)
    if content_volume is not None:
        out += f" × {_fmt_num(content_volume)}"
        if unit:
            out += f" {unit}"
    return out


def _fmt_num(value: Any) -> str:
    """Trim trailing .0 so ``3.0`` displays as ``3`` but ``1.5`` survives."""
    try:
        f = float(value)
    except (TypeError, ValueError):
        return str(value)
    if f.is_integer():
        return str(int(f))
    return ("%g" % f)


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
                bb = datetime.strptime(earliest, "%Y-%m-%d").date()
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


class PantristNextExpirationSensor(PantristEntity, SensorEntity):
    """Date/time of the next-expiring pantry item — drives Lovelace countdowns."""

    _attr_icon = "mdi:calendar-clock"
    _attr_translation_key = "next_expiration"
    _attr_device_class = SensorDeviceClass.TIMESTAMP
    # Derived metadata about the pantry — not an independent thing the user
    # interacts with, so park it under the diagnostic section of the device.
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, coordinator: PantristCoordinator) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.list_id}_{SENSOR_NEXT_EXPIRATION}"

    @property
    def native_value(self) -> datetime | None:
        """Earliest best-before across all pantry items, as a UTC datetime.

        Pantrist stores best-before as a calendar date — promote it to a
        timezone-aware datetime so HA's timestamp sensor class accepts it.
        Returns None if no pantry item has an earliest best-before.
        """
        earliest: date | None = None
        items = (self.coordinator.data.pantry or {}).get("items", [])
        for item in items:
            raw = (item.get("pantrySettings") or {}).get("earliestBestBefore")
            if not raw:
                continue
            try:
                bb = datetime.strptime(raw, "%Y-%m-%d").date()
            except (ValueError, TypeError):
                continue
            if earliest is None or bb < earliest:
                earliest = bb
        if earliest is None:
            return None
        return datetime.combine(earliest, time.min, tzinfo=timezone.utc)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        return {"list_id": self.coordinator.list_id}


class PantristLatestShoppingItemSensor(PantristEntity, SensorEntity):
    """Name of the most-recently added shopping-list item.

    Falls back to None (shown as unknown) when the list is empty.
    The image_url attribute lets picture-entity cards display the item's
    product image when one is available.
    """

    _attr_icon = "mdi:cart-arrow-down"
    _attr_translation_key = SENSOR_LATEST_SHOPPING_ITEM

    def __init__(self, coordinator: PantristCoordinator) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.list_id}_{SENSOR_LATEST_SHOPPING_ITEM}"

    @property
    def native_value(self) -> str | None:
        items = self.coordinator.data.shopping_list.get("items", [])
        if not items:
            return None
        return items[0].get("name") or None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        items = self.coordinator.data.shopping_list.get("items", [])
        if not items:
            return {"image_url": None}
        item = items[0]
        return {
            "image_url": item.get("imageUrl"),
            "uuid": item.get("uuid"),
            "display": _format_item(item).get("display"),
        }
