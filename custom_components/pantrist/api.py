"""Async Pantrist HTTP API wrapper.

Uses HA's shared aiohttp client and the OAuth2Session for bearer-token auth.
Each call returns the parsed JSON body or raises a PantristApiError subclass.
"""

from __future__ import annotations

import logging
from typing import Any

from aiohttp import ClientError, ClientResponseError
from homeassistant.core import HomeAssistant
from homeassistant.helpers import aiohttp_client
from homeassistant.helpers.config_entry_oauth2_flow import OAuth2Session

from .const import API_BASE

_LOGGER = logging.getLogger(__name__)


class PantristApiError(Exception):
    """Raised when an API call fails."""


class PantristAuthError(PantristApiError):
    """Raised on 401 — caller should trigger reauth."""


class PantristApi:
    """Async client for the Pantrist REST API."""

    def __init__(self, hass: HomeAssistant, session: OAuth2Session) -> None:
        self._session = session
        self._client = aiohttp_client.async_get_clientsession(hass)

    async def _request(
        self,
        method: str,
        path: str,
        *,
        json: Any | None = None,
    ) -> Any:
        await self._session.async_ensure_token_valid()
        token = self._session.token["access_token"]
        url = f"{API_BASE}{path}"
        try:
            async with self._client.request(
                method,
                url,
                headers={"Authorization": f"Bearer {token}"},
                json=json,
            ) as resp:
                if resp.status == 401:
                    raise PantristAuthError(f"401 from {method} {path}")
                if resp.status >= 400:
                    text = await resp.text()
                    raise PantristApiError(
                        f"{method} {path} → {resp.status}: {text[:200]}"
                    )
                if resp.status == 204 or not resp.content_length:
                    return None
                return await resp.json()
        except ClientResponseError as err:
            if err.status == 401:
                raise PantristAuthError(str(err)) from err
            raise PantristApiError(str(err)) from err
        except ClientError as err:
            raise PantristApiError(str(err)) from err

    # --- Lists ---

    async def get_lists(self) -> list[dict[str, Any]]:
        """Return all pantry blocks (lists) the user has access to."""
        data = await self._request("GET", "/list")
        return data or []

    # --- Shopping list ---

    async def get_shopping_list(self, list_id: str) -> dict[str, Any]:
        return await self._request("GET", f"/list/{list_id}/shoppingList")

    async def add_to_shopping_list_by_name(
        self, list_id: str, name: str
    ) -> dict[str, Any]:
        return await self._request(
            "POST",
            f"/list/{list_id}/shoppingList/add-by-name",
            json={"name": name},
        )

    async def check_shopping_list_item(self, list_id: str, item_id: str) -> None:
        await self._request(
            "POST", f"/list/{list_id}/shoppingList/{item_id}/check"
        )

    async def delete_shopping_list_item(self, list_id: str, item_id: str) -> None:
        await self._request(
            "DELETE", f"/list/{list_id}/shoppingList/{item_id}"
        )

    # --- Pantry list ---

    async def get_pantry_list(self, list_id: str) -> dict[str, Any]:
        return await self._request("GET", f"/list/{list_id}/pantryList")

    async def delete_pantry_item(self, list_id: str, item_id: str) -> None:
        await self._request("DELETE", f"/list/{list_id}/pantryList/{item_id}")

    async def change_pantry_item_amount(
        self, list_id: str, item_id: str, change: float, unit_id: str
    ) -> dict[str, Any]:
        return await self._request(
            "POST",
            f"/list/{list_id}/pantryList/{item_id}/change-amount",
            json={"change": change, "unit_id": unit_id},
        )

    # --- Shopping cart ---

    async def get_shopping_cart(self, list_id: str) -> list[dict[str, Any]]:
        data = await self._request("GET", f"/list/{list_id}/shoppingCart")
        return data or []
