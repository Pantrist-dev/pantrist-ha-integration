"""Amount strings read like the app's, with the list's own units."""

from __future__ import annotations

from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.pantrist.calendar import _describe_item as describe_event
from custom_components.pantrist.sensor import _format_item
from custom_components.pantrist.todo import _describe_item as describe_todo
from custom_components.pantrist.units import async_load_unit_labels, format_amount

from .conftest import LIST_ID

TUETE = {
    "uid": "u-tuete",
    "name": "Tüte(n)",
    "singular": "Tüte",
    "plural": "Tüten",
    "differentiation": True,
    "showAtItem": True,
}


async def _load(hass: HomeAssistant, language: str) -> None:
    hass.config.language = language
    await async_load_unit_labels(hass)


@pytest.mark.parametrize(
    ("amount", "volume", "unit", "expected"),
    [
        # A single piece shows nothing, like in the app.
        (1, 1, "pieces", None),
        (6, 1, "pieces", "6"),
        (2, 500, "g", "2 × 500 g"),
        (1, 500, "g", "500 g"),
        (1, 1, "l", "1 l"),
        (3, 1, "l", "3 × 1 l"),
        # Pieces with a content volume need the volume to make sense.
        (2, 8, "pieces", "2 × 8"),
        (1, 1, "packet", "1 Päckchen"),
        # The app spells out the content of one package for shown units.
        (2, 1, "packet", "2 × 1 Päckchen"),
        (1, 2, "tbsp", "2 EL"),
        (0, 1, "g", "0"),
        (None, 1, "g", None),
    ],
)
async def test_built_in_units_german(
    hass: HomeAssistant,
    amount: Any,
    volume: Any,
    unit: str,
    expected: str | None,
) -> None:
    await _load(hass, "de")
    assert format_amount(hass, {}, amount, volume, unit) == expected


async def test_built_in_units_english_singular_and_plural(hass: HomeAssistant) -> None:
    await _load(hass, "en")
    # One package of content 1 uses the unit's name, as the app does.
    assert format_amount(hass, {}, 1, 1, "packet") == "1 pack(s)"
    assert format_amount(hass, {}, 3, 2, "packet") == "3 × 2 packs"
    assert format_amount(hass, {}, 1, 2, "cup") == "2 cups"


async def test_saved_list_unit_wins(hass: HomeAssistant) -> None:
    await _load(hass, "de")
    units = {"u-tuete": TUETE}
    assert format_amount(hass, units, 1, 1, "u-tuete") == "1 Tüte(n)"
    assert format_amount(hass, units, 1, 5, "u-tuete") == "5 Tüten"
    assert format_amount(hass, units, 2, 5, "u-tuete") == "2 × 5 Tüten"
    # A list that renamed a built-in unit gets its own name.
    renamed = {"g": {"uid": "g", "name": "Gramm", "showAtItem": True}}
    assert format_amount(hass, renamed, 1, 250, "g") == "250 Gramm"
    # A saved unit that's hidden on items stays hidden; the package count
    # then tells "1 × 250" apart from a plain 250.
    hidden = {"g": {"uid": "g", "name": "g", "showAtItem": False}}
    assert format_amount(hass, hidden, 1, 250, "g") == "1 × 250"


async def test_unknown_unit_and_missing_translations(hass: HomeAssistant) -> None:
    await _load(hass, "de")
    assert format_amount(hass, {}, 2, 1, "bunch") == "2 × 1 bunch"
    # Without translations the uid itself is the label.
    assert format_amount(None, {}, 1, 1, "kg") == "1 kg"


async def test_descriptions_and_display(hass: HomeAssistant) -> None:
    await _load(hass, "de")
    units = {"u-tuete": TUETE}
    item = {"name": "Mehl", "amount": 2, "contentVolume": 3, "unitId": "u-tuete"}
    assert describe_todo(item, hass, units) == "2 × 3 Tüten"
    assert describe_event(item, hass, units) == "2 × 3 Tüten"
    formatted = _format_item(item, hass, units)
    assert formatted["display"] == "2 × 3 Tüten"
    # The raw id stays available for templates.
    assert formatted["unit"] == "u-tuete"
    # The display attribute still names a count when the app would show none.
    eggs = {"name": "Eier", "amount": 1, "contentVolume": 1, "unitId": "pieces"}
    assert describe_todo(eggs, hass, units) is None
    assert _format_item(eggs, hass, units)["display"] == "1"


@pytest.mark.usefixtures("mock_oauth_session", "mock_socketio")
async def test_setup_uses_the_lists_units(
    hass: HomeAssistant,
    config_entry: MockConfigEntry,
    mock_api: MagicMock,
) -> None:
    """The to-do list reads the list's units and German built-in labels.

    The count sensors' unit comes from the translation files too, but HA
    writes it into the state in the default language (the frontend shows the
    translated one), so the attribute stays ``items``.
    """
    hass.config.language = "de"
    mock_api.get_list_units = AsyncMock(return_value=[TUETE])
    mock_api.get_shopping_list = AsyncMock(
        return_value={
            "listId": LIST_ID,
            "items": [
                {"uuid": "i1", "name": "Mehl", "amount": 2, "contentVolume": 3,
                 "unitId": "u-tuete"},
                {"uuid": "i2", "name": "Butter", "amount": 1, "contentVolume": 1,
                 "unitId": "packet"},
                {"uuid": "i3", "name": "Eier", "amount": 1, "contentVolume": 1,
                 "unitId": "pieces"},
            ],
        }
    )

    config_entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    registry = er.async_get(hass)
    pantry = registry.async_get_entity_id("sensor", "pantrist", f"{LIST_ID}_pantry")
    todo = registry.async_get_entity_id(
        "todo", "pantrist", f"{LIST_ID}_shopping_list_todo"
    )
    assert pantry is not None and todo is not None

    state = hass.states.get(pantry)
    assert state is not None
    assert state.attributes["unit_of_measurement"] == "items"

    response = await hass.services.async_call(
        "todo",
        "get_items",
        target={"entity_id": todo},
        blocking=True,
        return_response=True,
    )
    assert response is not None
    items = response[todo]["items"]  # type: ignore[index]
    descriptions = [i.get("description") for i in items]
    assert descriptions == ["2 × 3 Tüten", "1 Päckchen", None]


@pytest.mark.usefixtures("mock_oauth_session", "mock_socketio")
async def test_failed_units_fetch_keeps_the_refresh(
    hass: HomeAssistant,
    config_entry: MockConfigEntry,
    mock_api: MagicMock,
) -> None:
    """Units only shape the text, so their endpoint failing is not fatal."""
    from custom_components.pantrist.api import PantristApiError

    mock_api.get_list_units = AsyncMock(side_effect=PantristApiError("boom"))

    config_entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    coordinator = config_entry.runtime_data[LIST_ID]
    assert coordinator.last_update_success
    assert coordinator.data.units == {}
