"""Sensor entity tests."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.pantrist.const import DOMAIN
from custom_components.pantrist.coordinator import PantristCoordinator, PantristData
from custom_components.pantrist.sensor import (
    PantristExpiringSoonSensor,
    PantristNextExpirationSensor,
    PantristPantrySensor,
    PantristShoppingCartSensor,
    PantristShoppingListSensor,
)

from .conftest import LIST_ID, LIST_NAME


@pytest.mark.usefixtures("mock_oauth_session", "mock_socketio")
async def test_sensors_materialize(
    hass: HomeAssistant,
    config_entry: MockConfigEntry,
    mock_api: MagicMock,
) -> None:
    """After setup the four sensors per list exist with sane state."""
    mock_api.get_shopping_list = AsyncMock(
        return_value={
            "listId": LIST_ID,
            "items": [{"uuid": "i1", "name": "Milk", "amount": 1, "unitId": "L"}],
        }
    )
    mock_api.get_pantry_list = AsyncMock(
        return_value={"listId": LIST_ID, "items": []}
    )
    mock_api.get_shopping_cart = AsyncMock(return_value=[])

    config_entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    registry = er.async_get(hass)
    unique_ids = {entry.unique_id for entry in registry.entities.values()}
    assert f"{LIST_ID}_shopping_list" in unique_ids
    assert f"{LIST_ID}_pantry" in unique_ids
    assert f"{LIST_ID}_expiring_soon" in unique_ids
    assert f"{LIST_ID}_shopping_cart" in unique_ids
    assert f"{LIST_ID}_next_expiration" in unique_ids
    # binary sensors + calendar materialise via the same setup
    assert f"{LIST_ID}_low_stock" in unique_ids
    assert f"{LIST_ID}_has_expired_items" in unique_ids
    assert f"{LIST_ID}_shopping_list_has_items" in unique_ids
    assert f"{LIST_ID}_pantry_calendar" in unique_ids


def _make_coordinator(hass: HomeAssistant, data: PantristData) -> PantristCoordinator:
    """Build a coordinator with arbitrary pre-loaded data — no HA setup needed."""
    coord = PantristCoordinator(hass, MagicMock(), MagicMock(), LIST_ID, LIST_NAME)
    coord.data = data
    return coord


async def test_shopping_list_sensor_state_and_attributes(hass: HomeAssistant) -> None:
    """Shopping list sensor exposes item count and a projected item list."""
    coord = _make_coordinator(
        hass,
        PantristData(
            shopping_list={
                "items": [
                    {
                        "uuid": "u1",
                        "name": "Milk",
                        "amount": 2,
                        "unitId": "L",
                        "brand": "Foo",
                        "categoryUuid": "cat-1",
                        "notes": "for the cat",
                        "imageUrl": "http://x/y.png",
                    }
                ]
            }
        ),
    )
    sensor = PantristShoppingListSensor(coord)
    assert sensor.native_value == 1
    attrs = sensor.extra_state_attributes
    assert attrs["list_id"] == LIST_ID
    assert attrs["items"][0]["name"] == "Milk"
    assert attrs["items"][0]["unit"] == "L"
    assert attrs["items"][0]["brand"] == "Foo"
    assert sensor.unique_id == f"{LIST_ID}_shopping_list"


async def test_pantry_sensor_reports_low_stock(hass: HomeAssistant) -> None:
    """Pantry sensor counts low-stock items separately."""
    coord = _make_coordinator(
        hass,
        PantristData(
            pantry={
                "items": [
                    {
                        "uuid": "p1",
                        "name": "Pasta",
                        "amount": 0,
                        "minimumAmount": 1,
                        "manageMinimumAmount": True,
                    },
                    {
                        "uuid": "p2",
                        "name": "Rice",
                        "amount": 5,
                        "minimumAmount": 1,
                        "manageMinimumAmount": True,
                    },
                    {
                        "uuid": "p3",
                        "name": "Salt",
                        "amount": 0,
                        "manageMinimumAmount": False,
                    },
                ]
            }
        ),
    )
    sensor = PantristPantrySensor(coord)
    assert sensor.native_value == 3
    attrs = sensor.extra_state_attributes
    assert attrs["low_stock_count"] == 1
    assert attrs["low_stock_items"][0]["name"] == "Pasta"


async def test_pantry_sensor_bulky_attrs_not_recorded(hass: HomeAssistant) -> None:
    """The large item lists are excluded from recorder history (16 KB cap).

    They stay in the live state for dashboards but must not be persisted, or
    the recorder logs "State attributes … exceed maximum size" and drops them.
    """
    coord = _make_coordinator(hass, PantristData(pantry={"items": []}))
    sensor = PantristPantrySensor(coord)
    assert {"items", "low_stock_items"} <= PantristPantrySensor._unrecorded_attributes
    # The attributes are still exposed live.
    assert "items" in sensor.extra_state_attributes


async def test_expiring_soon_sensor_splits_expiring_and_expired(
    hass: HomeAssistant,
) -> None:
    """Expiring-soon sensor categorises pantry items by best-before date."""
    from datetime import date, timedelta

    today = date.today()
    in_three = (today + timedelta(days=3)).strftime("%Y-%m-%d")
    yesterday = (today - timedelta(days=1)).strftime("%Y-%m-%d")
    far_future = (today + timedelta(days=99)).strftime("%Y-%m-%d")

    coord = _make_coordinator(
        hass,
        PantristData(
            pantry={
                "items": [
                    {
                        "uuid": "p1",
                        "name": "Yogurt",
                        "pantrySettings": {"earliestBestBefore": in_three},
                    },
                    {
                        "uuid": "p2",
                        "name": "Cheese",
                        "pantrySettings": {"earliestBestBefore": yesterday},
                    },
                    {
                        "uuid": "p3",
                        "name": "Flour",
                        "pantrySettings": {"earliestBestBefore": far_future},
                    },
                    {
                        "uuid": "p4",
                        "name": "Bread",
                        "pantrySettings": {"earliestBestBefore": "garbage"},
                    },
                    {
                        "uuid": "p5",
                        "name": "Sugar",
                        # no pantrySettings — skipped
                    },
                ]
            }
        ),
    )
    sensor = PantristExpiringSoonSensor(coord)
    # 1 expiring (Yogurt) + 1 expired (Cheese) = 2
    assert sensor.native_value == 2
    attrs = sensor.extra_state_attributes
    assert attrs["expiring_count"] == 1
    assert attrs["expired_count"] == 1
    assert attrs["expiring_items"][0]["name"] == "Yogurt"
    assert attrs["expired_items"][0]["name"] == "Cheese"
    assert attrs["warning_days"] == 7


async def test_shopping_cart_sensor(hass: HomeAssistant) -> None:
    """Shopping cart sensor flattens the article projection alongside cart metadata."""
    coord = _make_coordinator(
        hass,
        PantristData(
            shopping_cart=[
                {
                    "uuid": "c1",
                    "movedAt": "2026-05-20T10:00:00Z",
                    "article": {"uuid": "a1", "name": "Cucumber", "amount": 1},
                },
                {
                    "uuid": "c2",
                    "movedAt": "2026-05-20T10:05:00Z",
                    "article": None,
                },
            ]
        ),
    )
    sensor = PantristShoppingCartSensor(coord)
    assert sensor.native_value == 2
    items = sensor.extra_state_attributes["items"]
    assert items[0]["cart_uuid"] == "c1"
    assert items[0]["name"] == "Cucumber"
    assert items[1]["name"] == ""  # missing article


async def test_next_expiration_sensor_returns_earliest(hass: HomeAssistant) -> None:
    """The timestamp sensor picks the soonest valid best-before."""
    from datetime import date, timedelta

    today = date.today()
    in_three = (today + timedelta(days=3)).strftime("%Y-%m-%d")
    in_ten = (today + timedelta(days=10)).strftime("%Y-%m-%d")

    coord = _make_coordinator(
        hass,
        PantristData(
            pantry={
                "items": [
                    {"pantrySettings": {"earliestBestBefore": in_ten}},
                    {"pantrySettings": {"earliestBestBefore": in_three}},
                    {"pantrySettings": {"earliestBestBefore": "garbage"}},
                    {},  # no pantrySettings
                ]
            }
        ),
    )
    sensor = PantristNextExpirationSensor(coord)
    value = sensor.native_value
    assert value is not None
    assert value.date() == today + timedelta(days=3)
    assert sensor.unique_id == f"{LIST_ID}_next_expiration"
    assert sensor.extra_state_attributes["list_id"] == LIST_ID


async def test_next_expiration_sensor_returns_none_when_no_dates(
    hass: HomeAssistant,
) -> None:
    coord = _make_coordinator(hass, PantristData(pantry={"items": [{}, {}]}))
    assert PantristNextExpirationSensor(coord).native_value is None
