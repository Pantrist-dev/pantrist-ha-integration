"""Ingress-served web UI for the Pantrist HA add-on."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Protocol, TYPE_CHECKING

import aiohttp_jinja2
import jinja2
from aiohttp import web

if TYPE_CHECKING:
    from credentials import Credentials  # noqa: F401

logger = logging.getLogger(__name__)

TEMPLATE_DIR = Path(__file__).parent / "templates"


class AddonState(Protocol):
    """The set of operations ingress_server expects from main.py."""

    custom_ha_url: str
    session: object  # has is_running
    oauth_flow: object  # has begin/complete
    ha_client: object  # has post_persistent_notification

    def get_credentials(self): ...
    def save_credentials(self, creds): ...
    def clear_credentials(self): ...
    def start_session(self, creds): ...
    def stop_session(self): ...
    def get_list_name(self, list_id: str): ...


def _build_redirect_uri(request: web.Request, custom_ha_url: str) -> str:
    ingress_path = request.headers.get("X-Ingress-Path", "")
    if custom_ha_url:
        base = custom_ha_url.rstrip("/")
    else:
        proto = request.headers.get("X-Forwarded-Proto", "http")
        host = request.headers.get("Host", "homeassistant.local:8123")
        base = f"{proto}://{host}"
    return f"{base}{ingress_path}/oauth/callback"


def make_ingress_app(state) -> web.Application:
    app = web.Application()
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(str(TEMPLATE_DIR)))

    @aiohttp_jinja2.template("status.html")
    async def index(request: web.Request) -> dict:
        creds = state.get_credentials()
        list_name = state.get_list_name(creds.list_id) if creds else None
        return {
            "connected": creds is not None and state.session.is_running,
            "list_name": list_name,
            "ingress_path": request.headers.get("X-Ingress-Path", ""),
            "oauth_error": request.query.get("oauth_error"),
        }

    async def oauth_start(request: web.Request) -> web.Response:
        redirect_uri = _build_redirect_uri(request, state.custom_ha_url)
        url = state.oauth_flow.begin(redirect_uri)
        raise web.HTTPFound(location=url)

    async def oauth_callback(request: web.Request) -> web.Response:
        ingress_path = request.headers.get("X-Ingress-Path", "")
        if request.query.get("error"):
            raise web.HTTPFound(location=f"{ingress_path}/?oauth_error={request.query['error']}")
        if "code" not in request.query or "state" not in request.query:
            raise web.HTTPBadRequest(reason="missing_code_or_state")
        code = request.query["code"]
        req_state = request.query["state"]
        redirect_uri = _build_redirect_uri(request, state.custom_ha_url)
        try:
            creds = state.oauth_flow.complete(code=code, state=req_state, redirect_uri=redirect_uri)
        except Exception as exc:
            logger.exception("OAuth completion failed")
            raise web.HTTPFound(location=f"{ingress_path}/?oauth_error={exc}")
        state.save_credentials(creds)
        state.start_session(creds)
        raise web.HTTPFound(location=f"{ingress_path}/")

    async def disconnect(request: web.Request) -> web.Response:
        ingress_path = request.headers.get("X-Ingress-Path", "")
        state.stop_session()
        state.clear_credentials()
        try:
            state.ha_client.post_persistent_notification(
                notification_id="pantrist_disconnected",
                title="Pantrist",
                message="The Pantrist add-on was disconnected. Reconnect from the add-on UI.",
            )
        except Exception:
            logger.exception("notification on disconnect failed")
        raise web.HTTPFound(location=f"{ingress_path}/")

    app.router.add_get("/", index)
    app.router.add_get("/oauth/start", oauth_start)
    app.router.add_get("/oauth/callback", oauth_callback)
    app.router.add_post("/disconnect", disconnect)
    return app
