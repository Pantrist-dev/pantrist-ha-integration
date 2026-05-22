"""Pantrist calendar — pantry best-before dates.

One calendar entity per Pantrist list. Each pantry item with an
``earliestBestBefore`` becomes an all-day calendar event on that date,
so users can see upcoming expirations on the standard Lovelace calendar
card or set up template alerts off ``calendar.<list>_pantry``.
"""

from __future__ import annotations

from datetime import date, datetime, time, timedelta
import logging
from typing import Any

from homeassistant.components.calendar import CalendarEntity, CalendarEvent
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util import dt as dt_util

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
    """Add one pantry calendar per Pantrist list (dynamic)."""
    manager: PantristListManager = entry.runtime_data

    async_add_entities(
        PantristPantryCalendar(coordinator) for coordinator in manager.values()
    )

    @callback
    def _on_new_list(list_id: str) -> None:
        async_add_entities([PantristPantryCalendar(manager[list_id])])

    entry.async_on_unload(
        async_dispatcher_connect(
            hass, signal_new_list(entry.entry_id), _on_new_list
        )
    )


class PantristPantryCalendar(PantristEntity, CalendarEntity):
    """Pantry items as all-day calendar events on their best-before date."""

    _attr_icon = "mdi:calendar-alert"
    _attr_translation_key = "pantry_calendar"

    def __init__(self, coordinator: PantristCoordinator) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.list_id}_pantry_calendar"

    @property
    def event(self) -> CalendarEvent | None:
        """Next upcoming (or current) pantry expiration event.

        HA renders this on the entity's badge and tile view. Returns None
        if every pantry item is undated or already in the past.
        """
        today = dt_util.now().date()
        upcoming = sorted(
            (e for e in self._all_events() if e.start >= today),
            key=lambda e: e.start,
        )
        return upcoming[0] if upcoming else None

    async def async_get_events(
        self,
        hass: HomeAssistant,
        start_date: datetime,
        end_date: datetime,
    ) -> list[CalendarEvent]:
        """Events whose all-day date falls inside the requested window."""
        start = start_date.date()
        end = end_date.date()
        return [e for e in self._all_events() if start <= e.start <= end]

    def _all_events(self) -> list[CalendarEvent]:
        """Project current pantry data into a flat list of all-day events."""
        items = (self.coordinator.data.pantry or {}).get("items", [])
        events: list[CalendarEvent] = []
        for item in items:
            raw = (item.get("pantrySettings") or {}).get("earliestBestBefore")
            if not raw:
                continue
            try:
                bb = datetime.strptime(raw, "%Y-%m-%d").date()
            except (ValueError, TypeError):
                continue
            summary = item.get("name") or "Pantry item"
            events.append(
                CalendarEvent(
                    start=bb,
                    end=bb + timedelta(days=1),
                    summary=str(summary),
                    description=_describe_item(item),
                    uid=str(item.get("uuid") or f"{summary}-{raw}"),
                )
            )
        return events


def _describe_item(item: dict[str, Any]) -> str | None:
    """Compact one-liner with amount/unit/brand for the calendar event body."""
    parts: list[str] = []
    amount = item.get("amount")
    content_volume = item.get("contentVolume")
    unit = item.get("unitId")
    if amount is not None:
        def _n(v: Any) -> str:
            try:
                f = float(v)
                return str(int(f)) if f.is_integer() else f"{f:g}"
            except (TypeError, ValueError):
                return str(v)
        qty = _n(amount)
        if content_volume is not None:
            qty = f"{qty} × {_n(content_volume)}"
        if unit:
            qty += f" {unit}"
        parts.append(qty)
    brand = item.get("brand")
    if brand:
        parts.append(str(brand))
    return " · ".join(parts) if parts else None
