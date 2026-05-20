"""HTTP server for HA rest_command calls. Listens on port 8099."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Callable, Optional

from aiohttp import web

if TYPE_CHECKING:
    from pantrist_api import PantristAPI

logger = logging.getLogger(__name__)

APIProvider = Callable[[], Optional["PantristAPI"]]


def make_service_app(api_provider: APIProvider) -> web.Application:
    """Build an aiohttp app for rest_command endpoints.

    `api_provider` returns the current PantristAPI or None if the session is not running.
    """

    def _require_api() -> "PantristAPI":
        api = api_provider()
        if api is None:
            raise web.HTTPServiceUnavailable(reason="session_not_started")
        return api

    async def health(_request: web.Request) -> web.Response:
        return web.json_response({"status": "ok"})

    async def add_to_shopping_list(request: web.Request) -> web.Response:
        body = await request.json()
        result = _require_api().add_to_shopping_list_by_name(body["name"])
        return web.json_response(result if result else {"success": True})

    async def add_to_shopping_list_by_barcode(request: web.Request) -> web.Response:
        body = await request.json()
        result = _require_api().add_to_shopping_list_by_barcode(body["barcode"])
        return web.json_response(result if result else {"success": True})

    async def add_to_pantry(request: web.Request) -> web.Response:
        body = await request.json()
        result = _require_api().add_to_pantry_by_name(
            body["list_id"],
            body["name"],
            float(body.get("amount", 1)),
            body.get("unit_id", "pieces"),
        )
        return web.json_response(result if result else {"success": True})

    async def check_shopping_list_item(request: web.Request) -> web.Response:
        body = await request.json()
        _require_api().check_shopping_list_item(body["item_id"])
        return web.json_response({"success": True})

    async def delete_shopping_list_item(request: web.Request) -> web.Response:
        body = await request.json()
        _require_api().delete_shopping_list_item(body["list_id"], body["item_id"])
        return web.json_response({"success": True})

    async def delete_pantry_item(request: web.Request) -> web.Response:
        body = await request.json()
        _require_api().delete_pantry_item(body["list_id"], body["item_id"])
        return web.json_response({"success": True})

    async def change_pantry_amount(request: web.Request) -> web.Response:
        body = await request.json()
        result = _require_api().change_pantry_item_amount(
            body["list_id"],
            body["item_id"],
            float(body["change"]),
            body["unit_id"],
        )
        return web.json_response(result if result else {"success": True})

    app = web.Application()
    app.router.add_get("/health", health)
    app.router.add_post("/services/add_to_shopping_list", add_to_shopping_list)
    app.router.add_post(
        "/services/add_to_shopping_list_by_barcode", add_to_shopping_list_by_barcode
    )
    app.router.add_post("/services/add_to_pantry", add_to_pantry)
    app.router.add_post("/services/check_shopping_list_item", check_shopping_list_item)
    app.router.add_post("/services/delete_shopping_list_item", delete_shopping_list_item)
    app.router.add_post("/services/delete_pantry_item", delete_pantry_item)
    app.router.add_post("/services/change_pantry_item_amount", change_pantry_amount)
    return app
