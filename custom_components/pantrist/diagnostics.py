"""Diagnostics for the Pantrist integration.

Exposed via Settings → Devices & Services → Pantrist → Download diagnostics.
Includes the redacted config entry, per-list coordinator status, and a tiny
slice of the cached data so support requests have actionable context
without leaking tokens or item content.
"""

from __future__ import annotations

from typing import Any

from homeassistant.components.diagnostics import async_redact_data
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .coordinator import PantristCoordinator

REDACT_TOKEN_KEYS = {
    "access_token",
    "refresh_token",
    "code",
    "code_verifier",
    "code_challenge",
    "client_secret",
    "id_token",
}


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: ConfigEntry
) -> dict[str, Any]:
    """Return the diagnostics payload for one Pantrist entry."""

    coordinators: dict[str, PantristCoordinator] = (
        getattr(entry, "runtime_data", None) or {}
    )

    return {
        "entry": {
            "title": entry.title,
            "version": entry.version,
            "source": entry.source,
            "data": async_redact_data(dict(entry.data), REDACT_TOKEN_KEYS),
            "options": dict(entry.options),
        },
        "lists": {
            list_id: _coordinator_diagnostics(coord)
            for list_id, coord in coordinators.items()
        },
    }


def _coordinator_diagnostics(coordinator: PantristCoordinator) -> dict[str, Any]:
    """Compact per-list status summary."""
    data = coordinator.data
    return {
        "list_id": coordinator.list_id,
        "list_name": coordinator.list_name,
        "last_update_success": coordinator.last_update_success,
        "update_interval": str(coordinator.update_interval),
        "shopping_list_count": len((data.shopping_list or {}).get("items", [])) if data else 0,
        "pantry_count": len((data.pantry or {}).get("items", [])) if data else 0,
        "shopping_cart_count": len(data.shopping_cart) if data else 0,
    }
