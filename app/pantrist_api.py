"""Pantrist API client based on the OpenAPI specification."""

import logging
from typing import Any

import httpx

logger = logging.getLogger(__name__)

BASE_URL = "https://api.pantrist.app"


class PantristAPIError(Exception):
    pass


class PantristAPI:
    def __init__(self, token: str):
        self._headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        self._client = httpx.Client(headers=self._headers, timeout=30)

    def update_token(self, token: str) -> None:
        """Update the bearer token for all subsequent requests."""
        self._client.headers.update({"Authorization": f"Bearer {token}"})

    def _get(self, path: str) -> Any:
        response = self._client.get(f"{BASE_URL}{path}")
        response.raise_for_status()
        return response.json()

    def _post(self, path: str, body: dict | None = None) -> Any:
        response = self._client.post(f"{BASE_URL}{path}", json=body or {})
        response.raise_for_status()
        return response.json() if response.content else None

    def _put(self, path: str, body: dict) -> Any:
        response = self._client.put(f"{BASE_URL}{path}", json=body)
        response.raise_for_status()
        return response.json() if response.content else None

    def _delete(self, path: str) -> None:
        response = self._client.delete(f"{BASE_URL}{path}")
        response.raise_for_status()

    # --- Lists ---

    def get_lists(self) -> list[dict]:
        """Returns all lists the authenticated user has access to."""
        return self._get("/list")

    # --- Shopping List ---

    def get_current_shopping_list(self) -> dict:
        """Returns ItemListDto for the current shopping list."""
        return self._get("/shopping-list/current-list")

    def get_shopping_list(self, list_id: str) -> dict:
        """Returns ItemListDto for a specific shopping list."""
        return self._get(f"/shopping-list/{list_id}")

    def add_to_shopping_list_by_name(self, name: str) -> dict:
        """Adds an item to the current shopping list by name. Returns ArticleDto."""
        return self._post("/shopping-list/add-by-name", {"name": name})

    def check_shopping_list_item(self, item_id: str) -> None:
        """Checks off an item in the shopping list (marks as bought)."""
        self._post(f"/shopping-list/{item_id}/check")

    def delete_shopping_list_item(self, list_id: str, item_id: str) -> None:
        """Removes an item from the shopping list."""
        self._delete(f"/shopping-list/{list_id}/{item_id}")

    # --- Pantry List ---

    def get_current_pantry_list(self) -> dict:
        """Returns ItemListDto for the current pantry list."""
        return self._get("/pantry-list/current-list")

    def get_pantry_list(self, list_id: str) -> dict:
        """Returns ItemListDto for a specific pantry list."""
        return self._get(f"/pantry-list/{list_id}")

    def delete_pantry_item(self, list_id: str, item_id: str) -> None:
        """Removes an item from the pantry list."""
        self._delete(f"/pantry-list/{list_id}/{item_id}")

    def change_pantry_item_amount(
        self, list_id: str, item_id: str, change: float, unit_id: str
    ) -> dict:
        """Changes the amount of a pantry item by the given delta. Returns ItemDto."""
        return self._put(
            f"/pantry-list/change-amount/{list_id}/{item_id}",
            {"change": change, "unitId": unit_id},
        )

    # --- Shopping Cart ---

    def get_shopping_cart(self) -> dict:
        """Returns ItemListDto for the current user's shopping cart."""
        return self._get("/shopping-cart")

    # --- Barcodes ---

    def lookup_barcode(self, barcode: str) -> dict | None:
        """Returns BarcodeDto for the given barcode, or None if not found."""
        try:
            return self._get(f"/barcodes/{barcode}")
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 404:
                return None
            raise

    def add_to_shopping_list_by_barcode(self, barcode: str) -> dict:
        """Looks up a barcode and adds the matching article to the shopping list."""
        barcode_data = self.lookup_barcode(barcode)
        if barcode_data is None:
            raise PantristAPIError(f"Barcode not found: {barcode}")
        return self.add_to_shopping_list_by_name(barcode_data["name"])

    def add_to_pantry_by_name(
        self, name: str, amount: float = 1, unit_id: str = "pieces"
    ) -> dict:
        """Adds an item to the current pantry by name. Returns ArticleDto."""
        return self._post(
            "/pantry-list/add-by-name",
            {"name": name, "amount": amount, "unitId": unit_id},
        )

    # --- Storage Locations ---

    def get_current_storage_locations(self) -> list[dict]:
        """Returns all storage locations for the current list."""
        return self._get("/storage-location/current-list")

    def close(self) -> None:
        self._client.close()
