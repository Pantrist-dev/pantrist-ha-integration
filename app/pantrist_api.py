"""Pantrist API client — thin wrapper around the generated pantrist_client package.

Regenerate the underlying client whenever the API changes:
    python scripts/generate_openapi_client.py --python-only

The generated package lives at:
    homeassistant-addon/pantrist/app/pantrist_client/

This wrapper keeps the rest of the addon decoupled from the generated naming
conventions (e.g. shopping_list_controller_get_items → get_shopping_list).
"""

from __future__ import annotations

import logging
from typing import Any

from pantrist_client import AuthenticatedClient
from pantrist_client.api.barcode import barcode_controller_find_one
from pantrist_client.api.list import list_controller_get_list
from pantrist_client.api.pantry_list import (
    pantry_list_controller_change_amount_of_item,
    pantry_list_controller_delete_item_of_list,
    pantry_list_controller_get_items as pantry_get_current,
    pantry_list_controller_get_locations_by_list_id as pantry_get_by_id,
)
from pantrist_client.api.pantry_list_items import pantry_list_items_controller_add_by_name
from pantrist_client.api.shopping_cart import shopping_cart_items_controller_get_items
from pantrist_client.api.shopping_list import (
    shopping_list_controller_add,
    shopping_list_controller_check,
    shopping_list_controller_delete_item_of_list,
    shopping_list_controller_get_items as shopping_get_current,
    shopping_list_controller_get_locations_by_list_id as shopping_get_by_id,
)
from pantrist_client.models import AddByNameDto, ChangeAmountOfItemDto

logger = logging.getLogger(__name__)

BASE_URL = "https://api.pantrist.app"


class PantristAPIError(Exception):
    pass


class PantristAPI:
    def __init__(self, token: str) -> None:
        self._client = AuthenticatedClient(base_url=BASE_URL, token=token)

    def update_token(self, token: str) -> None:
        """Swap in a new bearer token (called after OAuth refresh)."""
        self._client = AuthenticatedClient(base_url=BASE_URL, token=token)

    # --- Lists ---

    def get_lists(self) -> list[Any]:
        return list_controller_get_list.sync(client=self._client) or []

    # --- Shopping list ---

    def get_current_shopping_list(self) -> Any:
        return shopping_get_current.sync(client=self._client)

    def get_shopping_list(self, list_id: str) -> Any:
        return shopping_get_by_id.sync(list_id=list_id, client=self._client)

    def add_to_shopping_list_by_name(self, name: str) -> Any:
        return shopping_list_controller_add.sync(
            client=self._client, body=AddByNameDto(name=name)
        )

    def check_shopping_list_item(self, item_id: str) -> None:
        shopping_list_controller_check.sync(id=item_id, client=self._client)

    def delete_shopping_list_item(self, list_id: str, item_id: str) -> None:
        shopping_list_controller_delete_item_of_list.sync(
            list_id=list_id, item_id=item_id, client=self._client
        )

    # --- Pantry list ---

    def get_current_pantry_list(self) -> Any:
        return pantry_get_current.sync(client=self._client)

    def get_pantry_list(self, list_id: str) -> Any:
        return pantry_get_by_id.sync(list_id=list_id, client=self._client)

    def delete_pantry_item(self, list_id: str, item_id: str) -> None:
        pantry_list_controller_delete_item_of_list.sync(
            list_id=list_id, item_id=item_id, client=self._client
        )

    def change_pantry_item_amount(
        self, list_id: str, item_id: str, change: float, unit_id: str
    ) -> Any:
        return pantry_list_controller_change_amount_of_item.sync(
            list_id=list_id,
            item_id=item_id,
            body=ChangeAmountOfItemDto(change=change, unit_id=unit_id),
            client=self._client,
        )

    # --- Shopping cart ---

    def get_shopping_cart(self, list_id: str) -> list[Any]:
        return shopping_cart_items_controller_get_items.sync(
            list_id=list_id, client=self._client
        ) or []

    # --- Pantry add-by-name (new list-scoped route) ---

    def add_to_pantry_by_name(
        self, list_id: str, name: str, amount: float = 1, unit_id: str = "pieces"
    ) -> Any:
        return pantry_list_items_controller_add_by_name.sync(
            list_id=list_id,
            body=AddByNameDto(name=name, amount=amount, unit_id=unit_id),
            client=self._client,
        )

    # --- Barcodes ---

    def lookup_barcode(self, barcode: str) -> Any | None:
        try:
            return barcode_controller_find_one.sync(barcode=barcode, client=self._client)
        except Exception:
            return None

    def add_to_shopping_list_by_barcode(self, barcode: str) -> Any:
        result = self.lookup_barcode(barcode)
        if result is None:
            raise PantristAPIError(f"Barcode not found: {barcode}")
        return self.add_to_shopping_list_by_name(result.name)

    def close(self) -> None:
        # AuthenticatedClient manages its own httpx session; nothing to close explicitly.
        pass
