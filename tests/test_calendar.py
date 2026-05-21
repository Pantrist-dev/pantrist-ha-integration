"""Pantry calendar tests."""

from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
from unittest.mock import MagicMock

from homeassistant.core import HomeAssistant
from homeassistant.util import dt as dt_util

from custom_components.pantrist.calendar import (
    PantristPantryCalendar,
    _describe_item,
)
from custom_components.pantrist.coordinator import PantristCoordinator, PantristData

from .conftest import LIST_ID, LIST_NAME


def _make_coordinator(hass: HomeAssistant, data: PantristData) -> PantristCoordinator:
    coord = PantristCoordinator(hass, MagicMock(), MagicMock(), LIST_ID, LIST_NAME)
    coord.data = data
    return coord


async def test_event_returns_next_upcoming(hass: HomeAssistant) -> None:
    today = dt_util.now().date()
    in_three = (today + timedelta(days=3)).strftime("%Y-%m-%d")
    in_ten = (today + timedelta(days=10)).strftime("%Y-%m-%d")
    yesterday = (today - timedelta(days=1)).strftime("%Y-%m-%d")

    coord = _make_coordinator(
        hass,
        PantristData(
            pantry={
                "items": [
                    {"uuid": "1", "name": "Eggs", "pantrySettings": {"earliestBestBefore": in_three}},
                    {"uuid": "2", "name": "Cheese", "pantrySettings": {"earliestBestBefore": in_ten}},
                    {"uuid": "3", "name": "Milk", "pantrySettings": {"earliestBestBefore": yesterday}},
                ]
            }
        ),
    )
    cal = PantristPantryCalendar(coord)
    event = cal.event
    assert event is not None
    assert event.summary == "Eggs"
    assert cal.unique_id == f"{LIST_ID}_pantry_calendar"


async def test_event_none_when_no_future(hass: HomeAssistant) -> None:
    yesterday = (dt_util.now().date() - timedelta(days=1)).strftime("%Y-%m-%d")
    coord = _make_coordinator(
        hass,
        PantristData(
            pantry={
                "items": [
                    {"uuid": "1", "name": "Old", "pantrySettings": {"earliestBestBefore": yesterday}},
                ]
            }
        ),
    )
    assert PantristPantryCalendar(coord).event is None


async def test_get_events_filters_to_window(hass: HomeAssistant) -> None:
    today = dt_util.now().date()
    in_three = (today + timedelta(days=3)).strftime("%Y-%m-%d")
    in_thirty = (today + timedelta(days=30)).strftime("%Y-%m-%d")

    coord = _make_coordinator(
        hass,
        PantristData(
            pantry={
                "items": [
                    {"uuid": "1", "name": "Eggs", "pantrySettings": {"earliestBestBefore": in_three}, "amount": 6, "unitId": "pieces"},
                    {"uuid": "2", "name": "Cheese", "pantrySettings": {"earliestBestBefore": in_thirty}},
                ]
            }
        ),
    )
    cal = PantristPantryCalendar(coord)
    window_start = datetime.combine(today, datetime.min.time(), tzinfo=timezone.utc)
    window_end = window_start + timedelta(days=7)
    events = await cal.async_get_events(hass, window_start, window_end)
    assert len(events) == 1
    assert events[0].summary == "Eggs"
    assert events[0].description == "6 pieces"


async def test_get_events_skips_undated_and_invalid(hass: HomeAssistant) -> None:
    coord = _make_coordinator(
        hass,
        PantristData(
            pantry={
                "items": [
                    {"uuid": "1", "name": "NoDate"},
                    {"uuid": "2", "name": "BadDate", "pantrySettings": {"earliestBestBefore": "garbage"}},
                ]
            }
        ),
    )
    cal = PantristPantryCalendar(coord)
    start = datetime.combine(date(2020, 1, 1), datetime.min.time(), tzinfo=timezone.utc)
    end = datetime.combine(date(2030, 1, 1), datetime.min.time(), tzinfo=timezone.utc)
    assert await cal.async_get_events(hass, start, end) == []


def test_describe_item_returns_none_for_empty() -> None:
    assert _describe_item({}) is None


def test_describe_item_with_brand_and_amount() -> None:
    out = _describe_item({"amount": 2, "unitId": "L", "brand": "Foo"})
    assert out == "2 L · Foo"
