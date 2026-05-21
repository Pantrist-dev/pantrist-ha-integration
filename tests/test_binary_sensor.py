"""Binary sensor tests."""

from __future__ import annotations

from datetime import date, timedelta
from unittest.mock import MagicMock

from homeassistant.core import HomeAssistant

from custom_components.pantrist.binary_sensor import (
    PantristHasExpiredBinarySensor,
    PantristLowStockBinarySensor,
    PantristShoppingListHasItemsBinarySensor,
)
from custom_components.pantrist.coordinator import PantristCoordinator, PantristData

from .conftest import LIST_ID, LIST_NAME


def _make_coordinator(hass: HomeAssistant, data: PantristData) -> PantristCoordinator:
    coord = PantristCoordinator(hass, MagicMock(), MagicMock(), LIST_ID, LIST_NAME)
    coord.data = data
    return coord


async def test_low_stock_off_when_all_above_minimum(hass: HomeAssistant) -> None:
    coord = _make_coordinator(
        hass,
        PantristData(
            pantry={
                "items": [
                    {"manageMinimumAmount": True, "amount": 5, "minimumAmount": 1},
                ]
            }
        ),
    )
    assert PantristLowStockBinarySensor(coord).is_on is False


async def test_low_stock_on_when_at_or_below_minimum(hass: HomeAssistant) -> None:
    coord = _make_coordinator(
        hass,
        PantristData(
            pantry={
                "items": [
                    {"manageMinimumAmount": True, "amount": 5, "minimumAmount": 1},
                    {"manageMinimumAmount": True, "amount": 0, "minimumAmount": 1},
                ]
            }
        ),
    )
    sensor = PantristLowStockBinarySensor(coord)
    assert sensor.is_on is True
    assert sensor.unique_id == f"{LIST_ID}_low_stock"


async def test_low_stock_ignores_unmanaged_items(hass: HomeAssistant) -> None:
    """Items without manageMinimumAmount must never trigger low_stock."""
    coord = _make_coordinator(
        hass,
        PantristData(
            pantry={
                "items": [
                    {"manageMinimumAmount": False, "amount": 0, "minimumAmount": 1},
                ]
            }
        ),
    )
    assert PantristLowStockBinarySensor(coord).is_on is False


async def test_has_expired_on_when_any_in_past(hass: HomeAssistant) -> None:
    yesterday = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
    coord = _make_coordinator(
        hass,
        PantristData(
            pantry={
                "items": [
                    {"pantrySettings": {"earliestBestBefore": yesterday}},
                ]
            }
        ),
    )
    sensor = PantristHasExpiredBinarySensor(coord)
    assert sensor.is_on is True
    assert sensor.unique_id == f"{LIST_ID}_has_expired_items"


async def test_has_expired_off_when_only_future(hass: HomeAssistant) -> None:
    tomorrow = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
    coord = _make_coordinator(
        hass,
        PantristData(
            pantry={
                "items": [
                    {"pantrySettings": {"earliestBestBefore": tomorrow}},
                    {"pantrySettings": {"earliestBestBefore": "garbage"}},
                    {},  # missing pantrySettings
                ]
            }
        ),
    )
    assert PantristHasExpiredBinarySensor(coord).is_on is False


async def test_shopping_list_has_items_off_when_empty(hass: HomeAssistant) -> None:
    coord = _make_coordinator(hass, PantristData(shopping_list={"items": []}))
    sensor = PantristShoppingListHasItemsBinarySensor(coord)
    assert sensor.is_on is False
    assert sensor.unique_id == f"{LIST_ID}_shopping_list_has_items"


async def test_shopping_list_has_items_on_when_non_empty(hass: HomeAssistant) -> None:
    coord = _make_coordinator(
        hass, PantristData(shopping_list={"items": [{"uuid": "x"}]})
    )
    assert PantristShoppingListHasItemsBinarySensor(coord).is_on is True
