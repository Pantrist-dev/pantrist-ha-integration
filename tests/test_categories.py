"""Category names read like the app's, built-in ones translated."""

from __future__ import annotations

from homeassistant.core import HomeAssistant

from custom_components.pantrist.categories import category_name, category_names
from custom_components.pantrist.units import async_load_unit_labels

SAVED = {
    "24": {"uuid": "24", "name": {"translationKey": "categories.24.name"}},
    "1": {"uuid": "1", "name": {"translationKey": "category.default"}},
    "c-own": {"uuid": "c-own", "name": "Vorrat Keller"},
}


async def _load(hass: HomeAssistant, language: str) -> None:
    hass.config.language = language
    await async_load_unit_labels(hass)


async def test_built_in_category_is_translated(hass: HomeAssistant) -> None:
    await _load(hass, "de")
    assert category_name(hass, SAVED, "24") == "Soßen"
    assert category_name(hass, SAVED, "1") == "Nicht kategorisiert"


async def test_own_category_keeps_its_name(hass: HomeAssistant) -> None:
    await _load(hass, "de")
    assert category_name(hass, SAVED, "c-own") == "Vorrat Keller"


async def test_built_in_category_the_list_never_saved(hass: HomeAssistant) -> None:
    """Lists that never edited their categories don't store the defaults."""
    await _load(hass, "en")
    assert category_name(hass, {}, 24) == "Sauces"


async def test_unknown_category(hass: HomeAssistant) -> None:
    await _load(hass, "en")
    assert category_name(hass, SAVED, "gone") is None
    assert category_name(hass, SAVED, None) is None


async def test_category_names_maps_every_saved_category(hass: HomeAssistant) -> None:
    await _load(hass, "en")
    assert category_names(hass, SAVED) == {
        "24": "Sauces",
        "1": "Uncategorized",
        "c-own": "Vorrat Keller",
    }
