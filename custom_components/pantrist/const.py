"""Constants for the Pantrist integration."""

from __future__ import annotations

from typing import Final

DOMAIN: Final = "pantrist"

# OAuth2 endpoints — must match the redirect-uri whitelist on the Pantrist API.
OAUTH2_AUTHORIZE: Final = "https://www.pantrist.app/oauth/authorize"
OAUTH2_TOKEN: Final = "https://api.pantrist.app/access-token/token"

# Public OAuth client identifier. PKCE-only, no client secret.
CLIENT_ID: Final = "pantrist-ha"

# API base URLs.
API_BASE: Final = "https://api.pantrist.app"
SOCKET_NAMESPACE: Final = "/lists"

# Stored config-entry keys.
CONF_LIST_ID: Final = "list_id"

# Sensor identifiers.
SENSOR_SHOPPING_LIST: Final = "shopping_list"
SENSOR_PANTRY: Final = "pantry"
SENSOR_EXPIRING_SOON: Final = "expiring_soon"
SENSOR_SHOPPING_CART: Final = "shopping_cart"
SENSOR_NEXT_EXPIRATION: Final = "next_expiration"
SENSOR_LATEST_SHOPPING_ITEM: Final = "latest_shopping_item"

# Service identifiers.
SERVICE_ADD_TO_SHOPPING_LIST: Final = "add_to_shopping_list"
SERVICE_ADD_TO_SHOPPING_LIST_BY_BARCODE: Final = "add_to_shopping_list_by_barcode"
SERVICE_CHECK_SHOPPING_LIST_ITEM: Final = "check_shopping_list_item"
SERVICE_DELETE_SHOPPING_LIST_ITEM: Final = "delete_shopping_list_item"
SERVICE_ADD_TO_PANTRY: Final = "add_to_pantry"
SERVICE_DELETE_PANTRY_ITEM: Final = "delete_pantry_item"
SERVICE_CHANGE_PANTRY_AMOUNT: Final = "change_pantry_item_amount"
SERVICE_SEARCH_PANTRY_ITEMS: Final = "search_pantry_items"
