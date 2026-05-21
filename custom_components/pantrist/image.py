"""Pantrist image entities.

One ``image.<list>_latest_shopping_item`` entity per Pantrist list,
exposing the ``imageUrl`` of the most-recent shopping-list item that
actually has one. Dashboards (Lovelace picture / picture-entity cards)
and automations (e.g. "show the latest item on the wall display") can
target this entity directly instead of reaching into the sensor
``items`` attribute.

If no shopping-list item carries an image, ``image_url`` returns None
and HA renders the entity as unavailable.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

from homeassistant.components.image import ImageEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddEntitiesCallback

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
    """One image entity per list, dynamic."""
    manager: PantristListManager = entry.runtime_data

    async_add_entities(
        PantristLatestShoppingItemImage(hass, coordinator)
        for coordinator in manager.values()
    )

    @callback
    def _on_new_list(list_id: str) -> None:
        async_add_entities(
            [PantristLatestShoppingItemImage(hass, manager[list_id])]
        )

    entry.async_on_unload(
        async_dispatcher_connect(
            hass, signal_new_list(entry.entry_id), _on_new_list
        )
    )


class PantristLatestShoppingItemImage(PantristEntity, ImageEntity):
    """Image of the first shopping-list item that has one."""

    _attr_translation_key = "latest_shopping_item"
    _attr_icon = "mdi:image"

    def __init__(
        self, hass: HomeAssistant, coordinator: PantristCoordinator
    ) -> None:
        PantristEntity.__init__(self, coordinator)
        ImageEntity.__init__(self, hass)
        self._attr_unique_id = f"{coordinator.list_id}_latest_shopping_item"
        # Cache the last URL we surfaced so we can bump ``image_last_updated``
        # only when the URL actually changes — HA cycles the static image
        # cache on that timestamp.
        self._last_url: str | None = None

    @property
    def image_url(self) -> str | None:
        items = (self.coordinator.data.shopping_list or {}).get("items", [])
        new_url: str | None = None
        for item in items:
            candidate = item.get("imageUrl")
            if candidate:
                new_url = str(candidate)
                break
        if new_url != self._last_url:
            self._last_url = new_url
            self._attr_image_last_updated = datetime.now(tz=timezone.utc)
        return new_url
