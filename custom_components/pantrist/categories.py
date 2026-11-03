"""Category names the way the Pantrist app shows them.

A list's categories come from ``GET /list/{id}/categories``. A category the
user named carries that name; one of the app's built-in categories carries a
translation key instead (``categories.24.name``, ``category.default`` for
"Uncategorized"), and its label lives in the translation files under
``selector.category_name``, keyed by the category's number — the same trick
``units.py`` uses for the built-in units.
"""

from __future__ import annotations

from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.translation import async_get_cached_translations

from .const import DOMAIN

# Translation key of the built-in "Uncategorized" category, uuid 1.
_DEFAULT_KEY = "category.default"
_UNCATEGORIZED = "1"


def _built_in_number(translation_key: str) -> str | None:
    """``categories.24.name`` → ``24``, ``category.default`` → ``1``."""
    if translation_key == _DEFAULT_KEY:
        return _UNCATEGORIZED
    parts = translation_key.split(".")
    if len(parts) == 3 and parts[0] == "categories" and parts[2] == "name":
        return parts[1]
    return None


def _built_in_label(hass: HomeAssistant | None, number: str) -> str | None:
    if hass is None:
        return None
    # Loaded with the unit labels (same translation category) at setup.
    strings = async_get_cached_translations(
        hass, hass.config.language, "selector", DOMAIN
    )
    return strings.get(
        f"component.{DOMAIN}.selector.category_name.options.{number}"
    )


def category_name(
    hass: HomeAssistant | None,
    categories: dict[str, dict[str, Any]] | None,
    category_uuid: Any,
) -> str | None:
    """Display name of a category, None when it can't be told.

    A uuid the list hasn't saved is looked up as a built-in category, since
    lists that never edited their categories don't store the defaults.
    """
    if category_uuid is None:
        return None
    uuid = str(category_uuid)
    saved = (categories or {}).get(uuid)
    if saved is None:
        return _built_in_label(hass, uuid)
    name = saved.get("name")
    if isinstance(name, str):
        return name or None
    if isinstance(name, dict):
        number = _built_in_number(str(name.get("translationKey") or ""))
        if number is not None:
            return _built_in_label(hass, number)
    return None


def category_names(
    hass: HomeAssistant | None, categories: dict[str, dict[str, Any]] | None
) -> dict[str, str]:
    """Every saved category of the list as uuid → display name."""
    out: dict[str, str] = {}
    for uuid in categories or {}:
        name = category_name(hass, categories, uuid)
        if name:
            out[uuid] = name
    return out
