"""Async Pantrist API wrapper built on the generated OpenAPI client.

Each public method:
  1. Refreshes the OAuth access token if needed (via OAuth2Session).
  2. Builds an AuthenticatedClient with the current bearer token.
  3. Calls the appropriate endpoint via its `.asyncio()` coroutine.
  4. Converts the typed DTO response to a plain dict for downstream sensors
     and coordinator consumers (so they keep the original JSON shape).

The generator (openapi-python-client 0.28.x) has two known bugs around
nullable / empty-enum response fields that the Pantrist API legitimately
produces — both are fixed by the post-process step in
`scripts/generate_client.py`. With that patch applied at generation time,
typed parsing here is safe.

Auth-failure (401) raises PantristAuthError so the coordinator can trigger
reauth via HA's standard `ConfigEntryAuthFailed` flow.
"""

from __future__ import annotations

import logging
from typing import Any

import httpx
from homeassistant.core import HomeAssistant
from homeassistant.helpers.config_entry_oauth2_flow import OAuth2Session
from homeassistant.util.ssl import client_context

from .const import API_BASE
from .pantrist_client import AuthenticatedClient
from .pantrist_client.api.barcode import barcode_controller_find_one
from .pantrist_client.api.list_ import list_controller_get_list
from .pantrist_client.api.list_units import (
    list_units_controller_get_units as _units_get,
)
from .pantrist_client.api.pantry_list import (
    pantry_list_items_controller_add_by_name,
    pantry_list_items_controller_change_amount,
    pantry_list_items_controller_delete_item,
    pantry_list_items_controller_get_item as _pantry_get_item,
    pantry_list_items_controller_get_items as _pantry_get_items,
    pantry_list_items_controller_upsert_item as _pantry_upsert_item,
)
from .pantrist_client.api.shopping_cart import (
    shopping_cart_items_controller_get_items as _cart_get_items,
)
from .pantrist_client.api.shopping_list import (
    shopping_list_items_controller_add_by_barcode,
    shopping_list_items_controller_add_by_name,
    shopping_list_items_controller_check_item,
    shopping_list_items_controller_delete_item,
    shopping_list_items_controller_get_items as _shopping_get_items,
)
from .pantrist_client.models import (
    AddByBarcodeDto,
    AddByNameDto,
    AddPantryByNameDto,
    ArticleDto,
    ChangeAmountOfItemDto,
)

_LOGGER = logging.getLogger(__name__)


_UNSET: Any = object()


def apply_pantry_item_changes(
    current: dict[str, Any], changes: dict[str, Any]
) -> dict[str, Any]:
    """Merge ``changes`` into an article dict for the full-upsert PUT.

    Plain fields (``name``, ``brand``, ``notes``, ``unitId``,
    ``contentVolume``, ``minimumAmountMode``) are copied over; None clears
    the nullable ones. Setting ``minimumAmount`` also switches tracking on
    unless ``manageMinimumAmount`` says otherwise. ``bestBefore`` lives per
    stock batch in ``pantrySettings.articleList``, so a new date goes to
    every batch and into ``earliestBestBefore``, and counts as user-set from
    then on. Same rules as ``applyPantryItemChanges`` in the Pantrist MCP.
    """
    changes = dict(changes)
    best_before = changes.pop("bestBefore", _UNSET)
    minimum = changes.pop("minimumAmount", _UNSET)
    manage = changes.pop("manageMinimumAmount", _UNSET)
    merged = {**current, **changes}

    if minimum is not _UNSET:
        merged["minimumAmount"] = minimum
        merged["manageMinimumAmount"] = True if manage is _UNSET else manage
    elif manage is not _UNSET:
        merged["manageMinimumAmount"] = manage

    if best_before is not _UNSET:
        settings = dict(current.get("pantrySettings") or {})
        # No batch yet: '1' is the default pantry every item lands in.
        batches = settings.get("articleList") or [
            {"pantryUuid": "1", "count": current.get("amount") or 0}
        ]
        article_list = []
        for batch in batches:
            rest = {
                k: v
                for k, v in batch.items()
                if k not in ("bestBefore", "calculatedBestBeforeDate")
            }
            if best_before is not None:
                rest.update(bestBefore=best_before, calculatedBestBeforeDate=False)
            article_list.append(rest)
        settings.pop("earliestBestBefore", None)
        settings["articleList"] = article_list
        if best_before is not None:
            settings["earliestBestBefore"] = best_before
        merged["pantrySettings"] = settings

    return merged


class PantristApiError(Exception):
    """Raised when an API call fails."""


class PantristAuthError(PantristApiError):
    """Raised on 401 — caller should trigger reauth."""


class PantristApi:
    """Async client for the Pantrist REST API (via generated OpenAPI client)."""

    def __init__(self, hass: HomeAssistant, session: OAuth2Session) -> None:
        self._hass = hass
        self._session = session
        self._httpx_client: httpx.AsyncClient | None = None

    async def _async_httpx_client(self) -> httpx.AsyncClient:
        """Return a lazily-built, reusable ``httpx.AsyncClient``.

        Constructing an ``httpx.AsyncClient`` makes httpx read the certifi CA
        bundle and call ``ssl.SSLContext.load_verify_locations()`` — a blocking
        file read. Done lazily on the first API call it lands inside the event
        loop, which HA detects and aborts the setup over.

        We sidestep that by building the SSL context once in the executor (via
        HA's cached ``client_context`` helper) and handing the ready-made
        context to httpx, so no blocking disk read ever runs in the loop. The
        client is reused across calls (connection pooling) and closed in
        :meth:`async_close` when the config entry unloads.
        """
        if self._httpx_client is None:
            ssl_context = await self._hass.async_add_executor_job(client_context)
            self._httpx_client = httpx.AsyncClient(
                base_url=API_BASE, verify=ssl_context
            )
        return self._httpx_client

    async def _client(self) -> AuthenticatedClient:
        """Return an AuthenticatedClient with a freshly-refreshed token."""
        await self._session.async_ensure_token_valid()
        token = self._session.token["access_token"]
        httpx_client = await self._async_httpx_client()
        # The generated client only stamps the auth header while *constructing*
        # its own httpx client; since we inject a pre-built one, set the bearer
        # ourselves. Concurrent calls (e.g. the coordinator's gather) share the
        # same refreshed token, so this write is idempotent and race-free.
        httpx_client.headers["Authorization"] = f"Bearer {token}"
        client = AuthenticatedClient(base_url=API_BASE, token=token)
        client.set_async_httpx_client(httpx_client)
        return client

    async def async_close(self) -> None:
        """Close the shared httpx client. Called when the config entry unloads."""
        if self._httpx_client is not None:
            await self._httpx_client.aclose()
            self._httpx_client = None

    @staticmethod
    def _wrap(value: Any) -> Any:
        """Call to_dict() if the value is an attrs DTO, else passthrough."""
        if value is None:
            return None
        if hasattr(value, "to_dict"):
            return value.to_dict()
        if isinstance(value, list):
            return [
                item.to_dict() if hasattr(item, "to_dict") else item for item in value
            ]
        return value

    async def _call(self, coro: Any) -> Any:
        """Await a generated endpoint coroutine, translating errors."""
        try:
            return await coro
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 401:
                raise PantristAuthError("401 from Pantrist API") from exc
            raise PantristApiError(
                f"{exc.response.status_code}: {exc.response.text[:200]}"
            ) from exc
        except httpx.RequestError as exc:
            raise PantristApiError(str(exc)) from exc

    # ------------------------------------------------------------------
    # Lists (account-wide)
    # ------------------------------------------------------------------

    async def get_lists(self) -> list[dict[str, Any]]:
        """Return all pantry blocks (lists) the user has access to.

        ``None`` is an error, not an empty account. The generated client runs
        with ``raise_on_unexpected_status`` off, so it answers any non-2xx by
        returning ``None`` rather than raising; a genuinely empty account
        comes back as an empty list. Reading ``None`` as "no lists" let a 401
        or a 502 look like the user having deleted everything, and the
        reconcile loop then removed every device and its entities.
        """
        client = await self._client()
        result = await self._call(list_controller_get_list.asyncio(client=client))
        if result is None:
            raise PantristApiError("The lists endpoint did not return a list")
        return self._wrap(result) or []

    async def get_list_units(self, list_id: str) -> list[dict[str, Any]]:
        """GET /list/{list_id}/units — the units the list has saved.

        Empty when the list never customised its units; the app then falls
        back to its built-in ones, and so do we (see ``units.py``).
        """
        client = await self._client()
        result = await self._call(_units_get.asyncio(client=client, list_id=list_id))
        if result is None:
            raise PantristApiError("The units endpoint did not return a list")
        return self._wrap(result) or []

    # ------------------------------------------------------------------
    # Shopping list
    # ------------------------------------------------------------------

    async def get_shopping_list(self, list_id: str) -> dict[str, Any]:
        """GET /list/{list_id}/shoppingList — items wrapped under `items` key."""
        client = await self._client()
        items = await self._call(
            _shopping_get_items.asyncio(client=client, list_id=list_id)
        )
        return {"listId": list_id, "items": self._wrap(items) or []}

    async def add_to_shopping_list_by_name(
        self, list_id: str, name: str
    ) -> dict[str, Any]:
        client = await self._client()
        result = await self._call(
            shopping_list_items_controller_add_by_name.asyncio(
                client=client, list_id=list_id, body=AddByNameDto(name=name)
            )
        )
        return self._wrap(result) or {}

    async def add_to_shopping_list_by_barcode(
        self, list_id: str, barcode: str
    ) -> dict[str, Any]:
        client = await self._client()
        result = await self._call(
            shopping_list_items_controller_add_by_barcode.asyncio(
                client=client, list_id=list_id, body=AddByBarcodeDto(barcode=barcode)
            )
        )
        return self._wrap(result) or {}

    async def check_shopping_list_item(self, list_id: str, item_id: str) -> None:
        client = await self._client()
        # Void endpoints only expose `asyncio_detailed` from the generator.
        await self._call(
            shopping_list_items_controller_check_item.asyncio_detailed(
                client=client, list_id=list_id, item_id=item_id
            )
        )

    async def delete_shopping_list_item(self, list_id: str, item_id: str) -> None:
        client = await self._client()
        await self._call(
            shopping_list_items_controller_delete_item.asyncio_detailed(
                client=client, list_id=list_id, item_id=item_id
            )
        )

    # ------------------------------------------------------------------
    # Pantry list
    # ------------------------------------------------------------------

    async def get_pantry_list(self, list_id: str) -> dict[str, Any]:
        """GET /list/{list_id}/pantryList — items wrapped under `items` key."""
        client = await self._client()
        items = await self._call(
            _pantry_get_items.asyncio(client=client, list_id=list_id)
        )
        return {"listId": list_id, "items": self._wrap(items) or []}

    async def add_to_pantry_by_name(
        self,
        list_id: str,
        name: str,
        amount: float = 1.0,
        unit_id: str = "pieces",
    ) -> dict[str, Any]:
        """Add a pantry item by name."""
        client = await self._client()
        dto = AddPantryByNameDto(name=name, amount=amount, unit_id=unit_id)
        result = await self._call(
            pantry_list_items_controller_add_by_name.asyncio(
                client=client, list_id=list_id, body=dto
            )
        )
        return self._wrap(result) or {}

    async def delete_pantry_item(self, list_id: str, item_id: str) -> None:
        client = await self._client()
        await self._call(
            pantry_list_items_controller_delete_item.asyncio_detailed(
                client=client, list_id=list_id, item_id=item_id
            )
        )

    async def update_pantry_item(
        self,
        list_id: str,
        item_id: str,
        changes: dict[str, Any],
        *,
        amount: float | None = None,
    ) -> dict[str, Any]:
        """Change a pantry item and leave everything else as it is.

        ``changes`` holds ArticleDto fields (see ``apply_pantry_item_changes``).
        The API only takes whole articles, so the item is read and PUT back
        with them applied, the same round-trip the Pantrist MCP's
        ``update_pantry_item`` does; a change made in the app between the two
        calls is lost. A new ``amount`` goes through the amount endpoint as a
        delta instead, like the number entities, because the stock batches in
        ``pantrySettings`` have to add up to it.
        """
        client = await self._client()
        article = await self._call(
            _pantry_get_item.asyncio(client=client, list_id=list_id, item_id=item_id)
        )
        if article is None:
            raise PantristApiError(f"Pantry item {item_id} was not found")
        current: dict[str, Any] = article.to_dict()
        result = current
        if changes:
            merged = apply_pantry_item_changes(current, changes)
            saved = await self._call(
                _pantry_upsert_item.asyncio(
                    client=client,
                    list_id=list_id,
                    item_id=item_id,
                    body=ArticleDto.from_dict(merged),
                )
            )
            result = self._wrap(saved) or merged
        if amount is not None:
            delta = amount - float(current.get("amount") or 0)
            if delta:
                result = await self.change_pantry_item_amount(
                    list_id, item_id, change=delta
                )
        return result

    async def change_pantry_item_amount(
        self,
        list_id: str,
        item_id: str,
        change: float,
        unit_id: str | None = None,  # accepted but unused by the modern endpoint
        product_group_index: float | None = None,
        pantry_id: str | None = None,
        auto_restock: bool = False,
    ) -> dict[str, Any]:
        """Change a pantry item's amount.

        The modern endpoint takes ``amount_change`` (delta) plus optional
        ``product_group_index`` / ``pantry_id`` for multi-group items.
        ``unit_id`` from the legacy signature is accepted but ignored.

        ``auto_restock`` opts into server-side
        "consume + add-to-shopping-list" behaviour: when set and the
        decrement crosses the item's ``minimumAmount``, the Pantrist API
        also adds a fully-populated copy of the article (category, brand,
        unit, image, …) to the shopping list. Use it for HA-driven flows
        like the NFC blueprint.
        """
        client = await self._client()
        kwargs: dict[str, Any] = {"amount_change": change}
        if product_group_index is not None:
            kwargs["product_group_index"] = product_group_index
        if pantry_id is not None:
            kwargs["pantry_id"] = pantry_id
        body = ChangeAmountOfItemDto(**kwargs)
        if auto_restock:
            # The generated client lags the backend by one DTO field; tunnel
            # the flag through ``additional_properties`` so it lands in the
            # JSON body without forcing a client regeneration on every API
            # bump.
            body.additional_properties["autoRestock"] = True
        result = await self._call(
            pantry_list_items_controller_change_amount.asyncio(
                client=client, list_id=list_id, item_id=item_id, body=body
            )
        )
        return self._wrap(result) or {}

    # ------------------------------------------------------------------
    # Shopping cart
    # ------------------------------------------------------------------

    async def get_shopping_cart(self, list_id: str) -> list[dict[str, Any]]:
        client = await self._client()
        items = await self._call(_cart_get_items.asyncio(client=client, list_id=list_id))
        return self._wrap(items) or []

    # ------------------------------------------------------------------
    # Barcodes (utility)
    # ------------------------------------------------------------------

    async def lookup_barcode(self, barcode: str) -> dict[str, Any] | None:
        """GET /barcodes/{barcode} — returns ArticleDto or None if unknown."""
        client = await self._client()
        result = await self._call(
            barcode_controller_find_one.asyncio(client=client, barcode=barcode)
        )
        wrapped: dict[str, Any] | None = self._wrap(result)
        return wrapped
