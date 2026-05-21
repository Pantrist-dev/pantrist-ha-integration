"""The Pantrist integration."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.exceptions import ConfigEntryAuthFailed, HomeAssistantError
from homeassistant.helpers import config_entry_oauth2_flow
import homeassistant.helpers.config_validation as cv

from .api import PantristApi, PantristApiError, PantristAuthError
from .const import (
    CONF_LIST_ID,
    DOMAIN,
    SERVICE_ADD_TO_PANTRY,
    SERVICE_ADD_TO_SHOPPING_LIST,
    SERVICE_ADD_TO_SHOPPING_LIST_BY_BARCODE,
    SERVICE_CHANGE_PANTRY_AMOUNT,
    SERVICE_CHECK_SHOPPING_LIST_ITEM,
    SERVICE_DELETE_PANTRY_ITEM,
    SERVICE_DELETE_SHOPPING_LIST_ITEM,
)
from .coordinator import PantristCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.TODO]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Pantrist from a config entry.

    One config entry corresponds to one Pantrist user account. After OAuth
    we enumerate every list the account has access to and create a separate
    PantristCoordinator (and therefore a separate HA Device) for each.

    Backward-compat: entries created before multi-list support have a
    `CONF_LIST_ID` in their data — in that case only that one list is
    surfaced, preserving existing entity IDs.
    """
    implementation = (
        await config_entry_oauth2_flow.async_get_config_entry_implementation(
            hass, entry
        )
    )
    session = config_entry_oauth2_flow.OAuth2Session(hass, entry, implementation)
    try:
        await session.async_ensure_token_valid()
    except Exception as err:
        raise ConfigEntryAuthFailed("OAuth token refresh failed") from err

    api = PantristApi(hass, session)

    try:
        lists = await api.get_lists()
    except PantristAuthError as err:
        raise ConfigEntryAuthFailed("Pantrist auth failed listing lists") from err
    except PantristApiError as err:
        _LOGGER.error("Failed to enumerate Pantrist lists: %s", err)
        return False

    # Single-list mode for legacy entries.
    legacy_list_id = entry.data.get(CONF_LIST_ID) or entry.data.get(
        "token", {}
    ).get("list_id")
    if legacy_list_id:
        lists = [li for li in lists if (li.get("id") or li.get("uuid")) == legacy_list_id]
        if not lists:
            _LOGGER.error(
                "Configured list_id %s not visible to this account — re-add the integration",
                legacy_list_id,
            )
            return False

    if not lists:
        _LOGGER.error(
            "Pantrist account has no lists yet — create one in the Pantrist app first"
        )
        return False

    coordinators: dict[str, PantristCoordinator] = {}
    for list_obj in lists:
        list_id = list_obj.get("id") or list_obj.get("uuid")
        if not list_id:
            continue
        list_name = list_obj.get("name")
        if not list_name:
            settings = list_obj.get("settings") or {}
            if isinstance(settings, dict):
                list_name = settings.get("name")
        coordinator = PantristCoordinator(hass, entry, api, list_id, list_name)
        await coordinator.async_config_entry_first_refresh()
        await coordinator.async_start_socketio()
        coordinators[list_id] = coordinator

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinators

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    _register_services(hass)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    coordinators: dict[str, PantristCoordinator] | None = hass.data.get(
        DOMAIN, {}
    ).get(entry.entry_id)
    if coordinators:
        for coordinator in coordinators.values():
            await coordinator.async_stop_socketio()

    unloaded = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unloaded:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unloaded


# ---------------------------------------------------------------------------
# Services
# ---------------------------------------------------------------------------


def _all_coordinators(hass: HomeAssistant) -> list[PantristCoordinator]:
    """Flatten every coordinator across every config entry."""
    out: list[PantristCoordinator] = []
    for entry_coords in hass.data.get(DOMAIN, {}).values():
        if isinstance(entry_coords, dict):
            out.extend(entry_coords.values())
    return out


def _coordinator_for_call(
    hass: HomeAssistant, list_id: str | None
) -> PantristCoordinator:
    """Resolve a service call to a coordinator.

    - If `list_id` is provided, that coordinator wins.
    - Otherwise pick the first available coordinator (single-list users
      don't have to specify anything).
    """
    coords = _all_coordinators(hass)
    if not coords:
        raise HomeAssistantError("Pantrist integration is not configured")
    if list_id:
        for c in coords:
            if c.list_id == list_id:
                return c
        raise HomeAssistantError(
            f"No Pantrist coordinator for list_id={list_id}. "
            f"Available: {[c.list_id for c in coords]}"
        )
    return coords[0]


def _register_services(hass: HomeAssistant) -> None:
    """Register Pantrist services once (idempotent)."""
    if hass.services.has_service(DOMAIN, SERVICE_ADD_TO_SHOPPING_LIST):
        return

    async def _call_api(
        call: ServiceCall, fn_name: str, **field_overrides: Any
    ) -> None:
        list_id = call.data.get("list_id")
        coordinator = _coordinator_for_call(hass, list_id)
        fn = getattr(coordinator.api, fn_name)
        try:
            await fn(coordinator.list_id, **field_overrides)
            await coordinator.async_request_refresh()
        except PantristAuthError as err:
            raise ConfigEntryAuthFailed("Pantrist auth failed") from err

    async def add_to_shopping_list(call: ServiceCall) -> None:
        await _call_api(call, "add_to_shopping_list_by_name", name=call.data["name"])

    async def add_to_shopping_list_by_barcode(call: ServiceCall) -> None:
        await _call_api(
            call,
            "add_to_shopping_list_by_barcode",
            barcode=call.data["barcode"],
        )

    async def check_shopping_list_item(call: ServiceCall) -> None:
        await _call_api(
            call, "check_shopping_list_item", item_id=call.data["item_id"]
        )

    async def delete_shopping_list_item(call: ServiceCall) -> None:
        await _call_api(
            call,
            "delete_shopping_list_item",
            item_id=call.data["item_id"],
        )

    async def add_to_pantry(call: ServiceCall) -> None:
        await _call_api(
            call,
            "add_to_pantry_by_name",
            name=call.data["name"],
            amount=float(call.data.get("amount", 1)),
            unit_id=call.data.get("unit_id", "pieces"),
        )

    async def delete_pantry_item(call: ServiceCall) -> None:
        await _call_api(
            call, "delete_pantry_item", item_id=call.data["item_id"]
        )

    async def change_pantry_amount(call: ServiceCall) -> None:
        await _call_api(
            call,
            "change_pantry_item_amount",
            item_id=call.data["item_id"],
            change=float(call.data["change"]),
            unit_id=call.data.get("unit_id"),
        )

    common = {vol.Optional("list_id"): cv.string}
    hass.services.async_register(
        DOMAIN,
        SERVICE_ADD_TO_SHOPPING_LIST,
        add_to_shopping_list,
        schema=vol.Schema({**common, vol.Required("name"): cv.string}),
    )
    hass.services.async_register(
        DOMAIN,
        SERVICE_ADD_TO_SHOPPING_LIST_BY_BARCODE,
        add_to_shopping_list_by_barcode,
        schema=vol.Schema({**common, vol.Required("barcode"): cv.string}),
    )
    hass.services.async_register(
        DOMAIN,
        SERVICE_CHECK_SHOPPING_LIST_ITEM,
        check_shopping_list_item,
        schema=vol.Schema({**common, vol.Required("item_id"): cv.string}),
    )
    hass.services.async_register(
        DOMAIN,
        SERVICE_DELETE_SHOPPING_LIST_ITEM,
        delete_shopping_list_item,
        schema=vol.Schema({**common, vol.Required("item_id"): cv.string}),
    )
    hass.services.async_register(
        DOMAIN,
        SERVICE_ADD_TO_PANTRY,
        add_to_pantry,
        schema=vol.Schema(
            {
                **common,
                vol.Required("name"): cv.string,
                vol.Optional("amount", default=1): vol.Coerce(float),
                vol.Optional("unit_id", default="pieces"): cv.string,
            }
        ),
    )
    hass.services.async_register(
        DOMAIN,
        SERVICE_DELETE_PANTRY_ITEM,
        delete_pantry_item,
        schema=vol.Schema({**common, vol.Required("item_id"): cv.string}),
    )
    hass.services.async_register(
        DOMAIN,
        SERVICE_CHANGE_PANTRY_AMOUNT,
        change_pantry_amount,
        schema=vol.Schema(
            {
                **common,
                vol.Required("item_id"): cv.string,
                vol.Required("change"): vol.Coerce(float),
                vol.Optional("unit_id"): cv.string,
            }
        ),
    )
