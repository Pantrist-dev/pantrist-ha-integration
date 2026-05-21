"""Image entity tests."""

from __future__ import annotations

from unittest.mock import MagicMock

from homeassistant.core import HomeAssistant

from custom_components.pantrist.coordinator import PantristCoordinator, PantristData
from custom_components.pantrist.image import PantristLatestShoppingItemImage

from .conftest import LIST_ID, LIST_NAME


def _make_coordinator(hass: HomeAssistant, data: PantristData) -> PantristCoordinator:
    coord = PantristCoordinator(hass, MagicMock(), MagicMock(), LIST_ID, LIST_NAME)
    coord.data = data
    return coord


async def test_image_url_returns_first_with_image(hass: HomeAssistant) -> None:
    coord = _make_coordinator(
        hass,
        PantristData(
            shopping_list={
                "items": [
                    {"uuid": "a", "name": "NoPic"},
                    {"uuid": "b", "name": "Milk", "imageUrl": "https://x/milk.png"},
                    {"uuid": "c", "name": "Eggs", "imageUrl": "https://x/eggs.png"},
                ]
            }
        ),
    )
    entity = PantristLatestShoppingItemImage(hass, coord)
    assert entity.image_url == "https://x/milk.png"
    assert entity.unique_id == f"{LIST_ID}_latest_shopping_item"


async def test_image_url_none_when_no_items_have_image(hass: HomeAssistant) -> None:
    coord = _make_coordinator(
        hass,
        PantristData(
            shopping_list={
                "items": [{"uuid": "a", "name": "NoPic"}],
            }
        ),
    )
    entity = PantristLatestShoppingItemImage(hass, coord)
    assert entity.image_url is None


async def test_image_url_change_bumps_last_updated(hass: HomeAssistant) -> None:
    coord = _make_coordinator(
        hass,
        PantristData(
            shopping_list={
                "items": [{"uuid": "a", "imageUrl": "https://x/1.png"}]
            }
        ),
    )
    entity = PantristLatestShoppingItemImage(hass, coord)
    assert entity.image_url == "https://x/1.png"
    first_ts = entity._attr_image_last_updated
    assert first_ts is not None

    # Same URL → timestamp unchanged.
    assert entity.image_url == "https://x/1.png"
    assert entity._attr_image_last_updated == first_ts

    # Change the URL — timestamp must bump.
    coord.data.shopping_list["items"][0]["imageUrl"] = "https://x/2.png"
    assert entity.image_url == "https://x/2.png"
    assert entity._attr_image_last_updated != first_ts
