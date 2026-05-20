"""Home Assistant REST API client for updating sensor states."""

import logging
import os
from datetime import date, datetime, timedelta
from typing import Any

import httpx

logger = logging.getLogger(__name__)

HA_API_URL = "http://supervisor/core/api"


class HAClient:
    def __init__(self) -> None:
        token = os.environ.get("SUPERVISOR_TOKEN", "")
        if not token:
            logger.warning("SUPERVISOR_TOKEN not set - HA state updates will fail")
        self._client = httpx.Client(
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
            timeout=10,
        )

    def set_state(
        self, entity_id: str, state: str, attributes: dict[str, Any] | None = None
    ) -> bool:
        """Create or update an entity state in Home Assistant."""
        payload: dict[str, Any] = {"state": state, "attributes": attributes or {}}
        try:
            response = self._client.post(
                f"{HA_API_URL}/states/{entity_id}", json=payload
            )
            response.raise_for_status()
            return True
        except httpx.HTTPStatusError as exc:
            logger.error(
                "Failed to set state for %s: HTTP %s - %s",
                entity_id,
                exc.response.status_code,
                exc.response.text,
            )
        except httpx.RequestError as exc:
            logger.error("Request error while updating %s: %s", entity_id, exc)
        return False

    def post_persistent_notification(
        self, notification_id: str, title: str, message: str
    ) -> None:
        """Best-effort HA persistent notification. Errors are logged, not raised."""
        token = os.environ.get("SUPERVISOR_TOKEN", "")
        try:
            response = httpx.post(
                "http://supervisor/core/api/services/persistent_notification/create",
                headers={"Authorization": f"Bearer {token}"},
                json={
                    "notification_id": notification_id,
                    "title": title,
                    "message": message,
                },
                timeout=10,
            )
            response.raise_for_status()
        except Exception:
            logger.exception("post_persistent_notification failed")

    def close(self) -> None:
        self._client.close()


def _format_item(item: dict) -> dict:
    """Extract a concise representation of an ArticleDto for HA attributes."""
    return {
        "uuid": item.get("uuid"),
        "name": item.get("name", ""),
        "amount": item.get("amount"),
        "unit": item.get("unitId"),
        "brand": item.get("brand"),
        "category_uuid": item.get("categoryUuid"),
        "notes": item.get("notes"),
        "image_url": item.get("imageUrl"),
    }


def build_shopping_list_state(data: dict) -> tuple[str, dict]:
    """Convert ItemListDto to (state, attributes) for sensor.pantrist_shopping_list."""
    items = data.get("items", [])
    return str(len(items)), {
        "friendly_name": "Pantrist Shopping List",
        "icon": "mdi:cart",
        "unit_of_measurement": "items",
        "list_id": data.get("listId"),
        "items": [_format_item(i) for i in items],
    }


def build_pantry_state(data: dict) -> tuple[str, dict]:
    """Convert ItemListDto to (state, attributes) for sensor.pantrist_pantry."""
    items = data.get("items", [])
    low_stock = [
        _format_item(i)
        for i in items
        if i.get("manageMinimumAmount")
        and i.get("amount", 0) <= i.get("minimumAmount", 0)
    ]
    return str(len(items)), {
        "friendly_name": "Pantrist Pantry",
        "icon": "mdi:fridge",
        "unit_of_measurement": "items",
        "list_id": data.get("listId"),
        "items": [_format_item(i) for i in items],
        "low_stock_count": len(low_stock),
        "low_stock_items": low_stock,
    }


def build_shopping_cart_state(items: list[dict]) -> tuple[str, dict]:
    """Convert ShoppingCartItemDto[] to (state, attributes) for sensor.pantrist_shopping_cart.

    Each ShoppingCartItemDto has shape: { uuid, article: ArticleDto, movedAt: number }.
    """
    formatted = [
        {
            "cart_uuid": i.get("uuid"),
            "moved_at": i.get("movedAt"),
            **_format_item(i.get("article") or {}),
        }
        for i in items
    ]
    return str(len(formatted)), {
        "friendly_name": "Pantrist Shopping Cart",
        "icon": "mdi:cart-check",
        "unit_of_measurement": "items",
        "items": formatted,
    }


def build_expiring_soon_state(data: dict, warning_days: int) -> tuple[str, dict]:
    """Derive expiring-soon sensor from pantry ItemListDto.

    Best-before dates are stored in pantrySettings.earliestBestBefore as DD-MM-YYYY.
    State = number of items expiring within warning_days OR already expired.
    """
    items = data.get("items", [])
    today = date.today()
    cutoff = today + timedelta(days=warning_days)

    expiring: list[dict] = []
    expired: list[dict] = []

    for item in items:
        settings = item.get("pantrySettings") or {}
        earliest = settings.get("earliestBestBefore")
        if not earliest:
            continue
        try:
            bb = datetime.strptime(earliest, "%d-%m-%Y").date()
        except (ValueError, TypeError):
            logger.debug("Unrecognised best-before format for '%s': %s", item.get("name"), earliest)
            continue

        formatted = {**_format_item(item), "best_before": earliest}
        if bb < today:
            expired.append(formatted)
        elif bb <= cutoff:
            expiring.append(formatted)

    expiring.sort(key=lambda x: x["best_before"])
    expired.sort(key=lambda x: x["best_before"])

    total = len(expiring) + len(expired)
    return str(total), {
        "friendly_name": "Pantrist Expiring Soon",
        "icon": "mdi:calendar-alert",
        "unit_of_measurement": "items",
        "warning_days": warning_days,
        "expiring_count": len(expiring),
        "expiring_items": expiring,
        "expired_count": len(expired),
        "expired_items": expired,
    }
