"""Amount strings the way the Pantrist app shows them.

A unit comes from the list's saved units (``GET /list/{id}/units``), which
carry the user's own name, singular and plural. A unit id the list hasn't
saved is one of the app's built-in units: its uid works as a translation
key, and the labels live in the translation files under
``selector.unit_name`` / ``unit_singular`` / ``unit_plural`` (HA has no
category for free text; selector options are the closest one hassfest
accepts).

``format_amount`` follows the app's ``AmountStringPipe``, minus opened
packages and storage-location filtering, which HA doesn't know about.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.translation import (
    async_get_cached_translations,
    async_get_translations,
)

from .const import DOMAIN

_CATEGORY = "selector"
_PIECES = "pieces"

# (differentiation, show_at_item) of the app's built-in units, from
# ``volumeUnitsParameter`` in the app's unit service.
_BUILT_IN: dict[str, tuple[bool, bool]] = {
    "Pinch": (True, False),
    "cup": (True, True),
    "fl-oz": (False, True),
    "g": (False, True),
    "gal": (False, True),
    "kg": (False, True),
    "l": (False, True),
    "lbs": (False, True),
    "ml": (False, True),
    "oz": (False, True),
    "packet": (True, True),
    "pieces": (True, False),
    "qt": (False, True),
    "tbsp": (False, True),
    "tsp": (False, True),
}


@dataclass(frozen=True)
class _Unit:
    name: str
    singular: str
    plural: str
    differentiation: bool
    show_at_item: bool


async def async_load_unit_labels(hass: HomeAssistant) -> None:
    """Warm HA's translation cache so the built-in labels resolve synchronously."""
    await async_get_translations(hass, hass.config.language, _CATEGORY, {DOMAIN})


def _built_in_label(hass: HomeAssistant | None, form: str, unit_id: str) -> str:
    if hass is None:
        return unit_id
    strings = async_get_cached_translations(
        hass, hass.config.language, _CATEGORY, DOMAIN
    )
    return strings.get(
        f"component.{DOMAIN}.{_CATEGORY}.unit_{form}.options.{unit_id}", unit_id
    )


def _resolve(
    hass: HomeAssistant | None,
    list_units: dict[str, dict[str, Any]],
    unit_id: str,
) -> _Unit:
    saved = list_units.get(unit_id)
    if saved is not None:
        name = saved.get("name") or unit_id
        return _Unit(
            name=name,
            singular=saved.get("singular") or name,
            plural=saved.get("plural") or name,
            differentiation=bool(saved.get("differentiation")),
            show_at_item=bool(saved.get("showAtItem")),
        )
    differentiation, show_at_item = _BUILT_IN.get(unit_id, (False, True))
    return _Unit(
        name=_built_in_label(hass, "name", unit_id),
        singular=_built_in_label(hass, "singular", unit_id),
        plural=_built_in_label(hass, "plural", unit_id),
        differentiation=differentiation,
        show_at_item=show_at_item,
    )


def _num(value: float) -> str:
    """Trim trailing .0 so ``3.0`` reads ``3`` but ``1.5`` survives."""
    return str(int(value)) if value.is_integer() else f"{value:g}"


def format_amount(
    hass: HomeAssistant | None,
    list_units: dict[str, dict[str, Any]] | None,
    amount: Any,
    content_volume: Any,
    unit_id: str | None,
) -> str | None:
    """Amount string for an item, e.g. ``2 × 500 g``; None when there is none.

    Like the app, a single package of a unit that isn't shown on items
    (``pieces`` by default) yields nothing rather than "1 × 1 pieces".
    """
    try:
        count = float(amount)
        volume = 1.0 if content_volume is None else float(content_volume)
    except (TypeError, ValueError):
        return None

    unit = _resolve(hass, list_units or {}, unit_id) if unit_id else None
    show_unit = unit is not None and unit.show_at_item
    needs_disambiguation = volume != 1 and not show_unit and count > 0
    show_count = count != 1 or needs_disambiguation

    out = _num(count) if show_count else ""
    if count > 0:
        if volume != 1 or (unit_id != _PIECES and show_unit):
            if show_count:
                out += " × "
            if volume:
                out += _num(volume)
            if unit is not None and show_unit:
                label = (
                    unit.plural if unit.differentiation and volume != 1 else unit.name
                )
                out += f" {label}"
        elif unit is not None and show_unit:
            if show_count:
                out += f" {unit.plural if unit.differentiation else unit.name}"
            else:
                label = unit.singular if unit.differentiation else unit.name
                out += f"{_num(count)} {label}"
    return out.strip() or None


def known_unit_ids(list_units: dict[str, dict[str, Any]] | None) -> list[str]:
    """Unit ids an item can use: the list's saved ones plus the built-in ones."""
    return sorted({*(list_units or {}), *_BUILT_IN})
