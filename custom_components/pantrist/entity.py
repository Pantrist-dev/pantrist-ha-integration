"""Common base entity for the Pantrist integration.

Every entity Pantrist exposes is tied to a single Pantrist list (one
PantristCoordinator instance), so we model each list as its own HA Device.
The integration's config entry then contains 0..N devices, one per list
the user wants to surface in Home Assistant.
"""

from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import PantristCoordinator


class PantristEntity(CoordinatorEntity[PantristCoordinator]):
    """Base for all Pantrist sensor / todo / button entities."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: PantristCoordinator) -> None:
        super().__init__(coordinator)
        list_id = coordinator.list_id
        list_name = coordinator.list_name or f"Pantrist (list {list_id[:8]}…)"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, list_id)},
            name=list_name,
            manufacturer="Pantrist",
            model="Shopping list & pantry",
            configuration_url="https://www.pantrist.app",
        )
