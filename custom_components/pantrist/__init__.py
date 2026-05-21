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

from .api import PantristApi, PantristAuthError
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

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Pantrist from a config entry."""
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

    list_id = entry.data.get(CONF_LIST_ID)
    if not list_id:
        # Fallback for entries created before list_id was stored as a top-level key.
        list_id = entry.data.get("token", {}).get("list_id")
    if not list_id:
        _LOGGER.error("No list_id in config entry — please re-add the integration")
        return False

    api = PantristApi(hass, session)
    coordinator = PantristCoordinator(hass, entry, api, list_id)
    await coordinator.async_config_entry_first_refresh()
    await coordinator.async_start_socketio()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    _register_services(hass)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    coordinator: PantristCoordinator | None = hass.data.get(DOMAIN, {}).get(
        entry.entry_id
    )
    if coordinator is not None:
        await coordinator.async_stop_socketio()

    unloaded = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unloaded:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unloaded


# ---------------------------------------------------------------------------
# Services
# ---------------------------------------------------------------------------


def _coordinator_for_call(hass: HomeAssistant) -> PantristCoordinator:
    """Return the first available coordinator. v1 assumes one entry per HA."""
    entries: dict[str, PantristCoordinator] = hass.data.get(DOMAIN, {})
    if not entries:
        raise HomeAssistantError("Pantrist integration is not configured")
    return next(iter(entries.values()))


def _register_services(hass: HomeAssistant) -> None:
    """Register Pantrist services once (idempotent)."""
    if hass.services.has_service(DOMAIN, SERVICE_ADD_TO_SHOPPING_LIST):
        return

    async def _call_api(call: ServiceCall, fn_name: str, **field_overrides: Any) -> None:
        coordinator = _coordinator_for_call(hass)
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

    hass.services.async_register(
        DOMAIN,
        SERVICE_ADD_TO_SHOPPING_LIST,
        add_to_shopping_list,
        schema=vol.Schema({vol.Required("name"): cv.string}),
    )
    hass.services.async_register(
        DOMAIN,
        SERVICE_ADD_TO_SHOPPING_LIST_BY_BARCODE,
        add_to_shopping_list_by_barcode,
        schema=vol.Schema({vol.Required("barcode"): cv.string}),
    )
    hass.services.async_register(
        DOMAIN,
        SERVICE_CHECK_SHOPPING_LIST_ITEM,
        check_shopping_list_item,
        schema=vol.Schema({vol.Required("item_id"): cv.string}),
    )
    hass.services.async_register(
        DOMAIN,
        SERVICE_DELETE_SHOPPING_LIST_ITEM,
        delete_shopping_list_item,
        schema=vol.Schema({vol.Required("item_id"): cv.string}),
    )
    hass.services.async_register(
        DOMAIN,
        SERVICE_ADD_TO_PANTRY,
        add_to_pantry,
        schema=vol.Schema(
            {
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
        schema=vol.Schema({vol.Required("item_id"): cv.string}),
    )
    hass.services.async_register(
        DOMAIN,
        SERVICE_CHANGE_PANTRY_AMOUNT,
        change_pantry_amount,
        schema=vol.Schema(
            {
                vol.Required("item_id"): cv.string,
                vol.Required("change"): vol.Coerce(float),
                vol.Optional("unit_id"): cv.string,
            }
        ),
    )
