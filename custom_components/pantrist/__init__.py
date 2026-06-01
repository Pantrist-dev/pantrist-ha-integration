"""The Pantrist integration."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import (
    HomeAssistant,
    ServiceCall,
    ServiceResponse,
    SupportsResponse,
)
from homeassistant.exceptions import (
    ConfigEntryAuthFailed,
    HomeAssistantError,
)
from homeassistant.helpers import config_entry_oauth2_flow
from homeassistant.helpers.config_entry_oauth2_flow import (
    LocalOAuth2ImplementationWithPkce,
    async_register_implementation,
)
from homeassistant.helpers.typing import ConfigType
import homeassistant.helpers.config_validation as cv

from .api import PantristApi, PantristApiError, PantristAuthError
from .const import (
    CLIENT_ID,
    DOMAIN,
    OAUTH2_AUTHORIZE,
    OAUTH2_TOKEN,
    SERVICE_ADD_TO_PANTRY,
    SERVICE_ADD_TO_SHOPPING_LIST,
    SERVICE_ADD_TO_SHOPPING_LIST_BY_BARCODE,
    SERVICE_CHANGE_PANTRY_AMOUNT,
    SERVICE_CHECK_SHOPPING_LIST_ITEM,
    SERVICE_DELETE_PANTRY_ITEM,
    SERVICE_DELETE_SHOPPING_LIST_ITEM,
    SERVICE_SEARCH_PANTRY_ITEMS,
)
from .coordinator import PantristCoordinator
from .list_manager import PantristListManager

# Bronze (runtime-data): the entry holds the per-list coordinator manager.
type PantristConfigEntry = ConfigEntry[PantristListManager]

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [
    Platform.BINARY_SENSOR,
    Platform.CALENDAR,
    Platform.NUMBER,
    Platform.SENSOR,
    Platform.TODO,
]

# Pure YAML config is not supported — this integration is config-flow only.
CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Register the PKCE implementation + Pantrist services.

    Registering via async_register_implementation (rather than
    async_import_client_credential) works without the application_credentials
    component — the implementation lives in hass.data and is found by
    async_get_implementations on every code path, including fresh installs
    where async_setup runs before the config flow.
    """
    async_register_implementation(
        hass,
        DOMAIN,
        LocalOAuth2ImplementationWithPkce(
            hass,
            DOMAIN,
            CLIENT_ID,
            authorize_url=OAUTH2_AUTHORIZE,
            token_url=OAUTH2_TOKEN,
            client_secret="",
        ),
    )
    _register_services(hass)
    return True


async def async_setup_entry(hass: HomeAssistant, entry: PantristConfigEntry) -> bool:
    """Set up Pantrist from a config entry.

    One config entry corresponds to one Pantrist user account. After OAuth
    we enumerate every list the account has access to and create a separate
    PantristCoordinator (and therefore a separate HA Device) for each.

    Backward-compat: entries created before multi-list support have a
    ``CONF_LIST_ID`` in their data — in that case only that one list is
    surfaced, preserving existing entity IDs. New entries see every list
    in the account, and new lists added in the Pantrist app appear in HA
    automatically within ``LIST_RECONCILE_INTERVAL``.
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
    manager = PantristListManager(hass, entry, api)
    try:
        await manager.async_initial_setup()
    except PantristApiError as err:
        _LOGGER.error("Pantrist setup failed: %s", err)
        return False

    entry.runtime_data = manager
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(
    hass: HomeAssistant, entry: PantristConfigEntry
) -> bool:
    """Unload a config entry — stops the reconcile loop and every coordinator."""
    manager = getattr(entry, "runtime_data", None)
    if manager is not None:
        await manager.async_shutdown()
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


# ---------------------------------------------------------------------------
# Services
# ---------------------------------------------------------------------------


def _all_coordinators(hass: HomeAssistant) -> list[PantristCoordinator]:
    """Flatten every coordinator across every Pantrist config entry."""
    out: list[PantristCoordinator] = []
    for entry in hass.config_entries.async_entries(DOMAIN):
        manager: PantristListManager | None = getattr(entry, "runtime_data", None)
        if manager is not None:
            out.extend(manager.values())
    return out


def _coordinator_for_call(
    hass: HomeAssistant, list_id: str | None
) -> PantristCoordinator:
    """Resolve a service call to a coordinator.

    - If ``list_id`` is provided, that coordinator wins.
    - Otherwise pick the first available coordinator (single-list users
      don't have to specify anything).
    """
    coords = _all_coordinators(hass)
    if not coords:
        raise HomeAssistantError(
            translation_domain=DOMAIN,
            translation_key="not_configured",
        )
    if list_id:
        for c in coords:
            if c.list_id == list_id:
                return c
        raise HomeAssistantError(
            translation_domain=DOMAIN,
            translation_key="unknown_list_id",
            translation_placeholders={
                "list_id": list_id,
                "available": ", ".join(c.list_id for c in coords),
            },
        )
    return coords[0]


def _pantry_items(coordinator: PantristCoordinator) -> list[dict[str, Any]]:
    """Pantry items from the coordinator snapshot that have a uuid and name."""
    return [
        item
        for item in (coordinator.data.pantry or {}).get("items", [])
        if item.get("uuid") and item.get("name")
    ]


def _match_pantry_items(
    items: list[dict[str, Any]], query: str
) -> list[dict[str, Any]]:
    """Match ``query`` against item names, case-insensitively.

    An exact (trimmed, case-folded) match wins outright; only when there is
    no exact match do we fall back to substring matches. Returns every item
    in the winning tier, in pantry order.
    """
    needle = query.strip().casefold()
    exact = [i for i in items if str(i["name"]).strip().casefold() == needle]
    if exact:
        return exact
    return [i for i in items if needle in str(i["name"]).strip().casefold()]


def _resolve_pantry_item_id(hass: HomeAssistant, call: ServiceCall) -> str:
    """Resolve a pantry item to its UUID for change_pantry_item_amount.

    Accepts either an explicit ``item_id`` (UUID, wins if given) or a
    human-friendly ``name`` that we look up against the live pantry — so
    automations and the action UI don't have to hunt for a UUID. Name
    matching is case-insensitive: an exact match wins, otherwise we fall
    back to a unique substring match. Ambiguous or missing matches raise a
    translatable HomeAssistantError listing what's available.
    """
    item_id = (call.data.get("item_id") or "").strip()
    if item_id:
        return item_id

    name = (call.data.get("name") or "").strip()
    if not name:
        raise HomeAssistantError(
            translation_domain=DOMAIN,
            translation_key="missing_item_identifier",
        )

    coordinator = _coordinator_for_call(hass, call.data.get("list_id"))
    items = _pantry_items(coordinator)
    matches = _match_pantry_items(items, name)

    if len(matches) == 1:
        return str(matches[0]["uuid"])

    if not matches:
        available = ", ".join(sorted(str(i["name"]) for i in items)) or "(none)"
        raise HomeAssistantError(
            translation_domain=DOMAIN,
            translation_key="pantry_item_not_found",
            translation_placeholders={"name": name, "available": available},
        )

    # More than one match — make the user disambiguate with a UUID.
    options = ", ".join(f"{i['name']} ({i['uuid']})" for i in matches)
    raise HomeAssistantError(
        translation_domain=DOMAIN,
        translation_key="pantry_item_ambiguous",
        translation_placeholders={"name": name, "matches": options},
    )


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
        except PantristAuthError as err:
            raise ConfigEntryAuthFailed("Pantrist auth failed") from err
        except PantristApiError as err:
            # Bronze (action-exceptions): never leak the integration-internal
            # exception type. Wrap it so callers see a HomeAssistantError
            # with a translatable message (Gold: exception-translations).
            raise HomeAssistantError(
                translation_domain=DOMAIN,
                translation_key="api_request_failed",
                translation_placeholders={"error": str(err)},
            ) from err
        await coordinator.async_request_refresh()

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
        item_id = _resolve_pantry_item_id(hass, call)
        await _call_api(
            call,
            "change_pantry_item_amount",
            item_id=item_id,
            change=float(call.data["change"]),
            auto_restock=bool(call.data.get("auto_restock", True)),
        )

    async def search_pantry_items(call: ServiceCall) -> ServiceResponse:
        """Return pantry items (and their UUIDs) matching an optional query.

        Read-only helper so users can discover the ``item_id`` to feed into
        change_pantry_item_amount — run it from Developer Tools → Actions to
        eyeball the UUID, or chain it in a script via ``response_variable``.
        With no ``query`` it returns the whole pantry.
        """
        coordinator = _coordinator_for_call(hass, call.data.get("list_id"))
        items = _pantry_items(coordinator)
        query = (call.data.get("query") or "").strip()
        if query:
            items = _match_pantry_items(items, query)
        return {
            "list_id": coordinator.list_id,
            "items": [
                {
                    "item_id": str(item["uuid"]),
                    "name": str(item["name"]),
                    "amount": item.get("amount"),
                    "unit": item.get("unitId"),
                }
                for item in items
            ],
        }

    # Annotated as dict[vol.Marker, Any] so mypy doesn't infer the narrower
    # marker subtype from the literal and reject the **spread below.
    common: dict[Any, Any] = {vol.Optional("list_id"): cv.string}
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
                # Identify the item by name (resolved against the live
                # pantry) or by raw UUID — at least one is required, which
                # is enforced in the handler so we can give a translatable
                # error rather than a raw voluptuous one.
                vol.Optional("name"): cv.string,
                vol.Optional("item_id"): cv.string,
                vol.Required("change"): vol.Coerce(float),
                # Defaults to True here even though the underlying API
                # defaults to False — the HA service is the automation
                # surface; a "consume + auto-reorder" round-trip is the
                # whole point. Callers who want bare decrement (e.g.
                # inventory-mode dashboards) pass ``auto_restock: false``.
                vol.Optional("auto_restock", default=True): cv.boolean,
            }
        ),
    )
    hass.services.async_register(
        DOMAIN,
        SERVICE_SEARCH_PANTRY_ITEMS,
        search_pantry_items,
        schema=vol.Schema({**common, vol.Optional("query"): cv.string}),
        supports_response=SupportsResponse.ONLY,
    )
