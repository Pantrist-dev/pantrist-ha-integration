"""Async Pantrist API wrapper built on the generated OpenAPI client.

Each public method:
  1. Refreshes the OAuth access token if needed (via OAuth2Session).
  2. Builds an AuthenticatedClient with the current bearer token.
  3. Calls the appropriate endpoint via its `.asyncio()` coroutine.
  4. Converts the typed DTO response to a plain dict for downstream sensors
     and coordinator consumers (so they keep the addon's existing JSON shape).

Auth-failure (401) raises PantristAuthError so the coordinator can request
reauth via HA's standard `ConfigEntryAuthFailed` flow.
"""

from __future__ import annotations

import logging
from typing import Any

import httpx
from homeassistant.core import HomeAssistant
from homeassistant.helpers.config_entry_oauth2_flow import OAuth2Session

from .const import API_BASE
from .pantrist_client import AuthenticatedClient
from .pantrist_client.api.barcode import barcode_controller_find_one
from .pantrist_client.api.list_ import list_controller_get_list
from .pantrist_client.api.pantry_list import (
    pantry_list_items_controller_add_by_name,
    pantry_list_items_controller_change_amount,
    pantry_list_items_controller_delete_item,
    pantry_list_items_controller_get_items as _pantry_get_items,
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
    ChangeAmountOfItemDto,
)

_LOGGER = logging.getLogger(__name__)


class PantristApiError(Exception):
    """Raised when an API call fails."""


class PantristAuthError(PantristApiError):
    """Raised on 401 — caller should trigger reauth."""


class PantristApi:
    """Async client for the Pantrist REST API (via generated OpenAPI client)."""

    def __init__(self, hass: HomeAssistant, session: OAuth2Session) -> None:
        self._hass = hass
        self._session = session

    async def _client(self) -> AuthenticatedClient:
        """Return an AuthenticatedClient with a freshly-refreshed token."""
        await self._session.async_ensure_token_valid()
        token = self._session.token["access_token"]
        return AuthenticatedClient(base_url=API_BASE, token=token)

    @staticmethod
    def _wrap(value: Any) -> Any:
        """Call to_dict() if the value is an attrs DTO, else passthrough."""
        if value is None:
            return None
        if hasattr(value, "to_dict"):
            return value.to_dict()
        if isinstance(value, list):
            return [item.to_dict() if hasattr(item, "to_dict") else item for item in value]
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
        """Return all pantry blocks (lists) the user has access to."""
        client = await self._client()
        result = await self._call(list_controller_get_list.asyncio(client=client))
        return self._wrap(result) or []

    # ------------------------------------------------------------------
    # Shopping list
    # ------------------------------------------------------------------

    async def get_shopping_list(self, list_id: str) -> dict[str, Any]:
        """GET /list/{list_id}/shoppingList — items wrapped under `items` key."""
        client = await self._client()
        items = await self._call(_shopping_get_items.asyncio(client=client, list_id=list_id))
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
        await self._call(
            shopping_list_items_controller_check_item.asyncio(
                client=client, list_id=list_id, item_id=item_id
            )
        )

    async def delete_shopping_list_item(self, list_id: str, item_id: str) -> None:
        client = await self._client()
        await self._call(
            shopping_list_items_controller_delete_item.asyncio(
                client=client, list_id=list_id, item_id=item_id
            )
        )

    # ------------------------------------------------------------------
    # Pantry list
    # ------------------------------------------------------------------

    async def get_pantry_list(self, list_id: str) -> dict[str, Any]:
        """GET /list/{list_id}/pantryList — items wrapped under `items` key."""
        client = await self._client()
        items = await self._call(_pantry_get_items.asyncio(client=client, list_id=list_id))
        return {"listId": list_id, "items": self._wrap(items) or []}

    async def add_to_pantry_by_name(
        self,
        list_id: str,
        name: str,
        amount: float = 1.0,
        unit_id: str = "pieces",
    ) -> dict[str, Any]:
        """Add a pantry item by name.

        amount/unit_id are accepted for backwards compat with the addon's
        service signature; the modern endpoint accepts only `name` so the
        extras land in `additional_properties` and are ignored server-side
        unless the API later adopts them.
        """
        client = await self._client()
        dto = AddByNameDto(name=name)
        if amount is not None:
            dto.additional_properties["amount"] = amount
        if unit_id is not None:
            dto.additional_properties["unitId"] = unit_id
        result = await self._call(
            pantry_list_items_controller_add_by_name.asyncio(
                client=client, list_id=list_id, body=dto
            )
        )
        return self._wrap(result) or {}

    async def delete_pantry_item(self, list_id: str, item_id: str) -> None:
        client = await self._client()
        await self._call(
            pantry_list_items_controller_delete_item.asyncio(
                client=client, list_id=list_id, item_id=item_id
            )
        )

    async def change_pantry_item_amount(
        self,
        list_id: str,
        item_id: str,
        change: float,
        unit_id: str | None = None,  # accepted but unused by the modern endpoint
        product_group_index: float | None = None,
        pantry_id: str | None = None,
    ) -> dict[str, Any]:
        """Change a pantry item's amount.

        The modern endpoint takes `amount_change` (delta) plus optional
        `product_group_index`/`pantry_id` for multi-group items. `unit_id`
        from the legacy signature is accepted but ignored.
        """
        client = await self._client()
        kwargs: dict[str, Any] = {"amount_change": change}
        if product_group_index is not None:
            kwargs["product_group_index"] = product_group_index
        if pantry_id is not None:
            kwargs["pantry_id"] = pantry_id
        body = ChangeAmountOfItemDto(**kwargs)
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
        return self._wrap(result)
