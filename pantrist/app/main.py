"""
Pantrist Home Assistant Add-on — entrypoint.

Two-phase bootstrap:
  1. Always-on web servers (ingress UI + rest_command service).
  2. Data pipeline (PantristSession) starts only when /data/credentials.json exists.

The user runs through an OAuth flow via the ingress UI to populate credentials;
on token-refresh failure or user disconnect, the data pipeline stops while the
web UI stays up so the user can reconnect.
"""

from __future__ import annotations

import asyncio
import json
import logging
import signal
import sys
from dataclasses import dataclass, field
from typing import Optional

from aiohttp import web

import credentials as creds_store
from credentials import Credentials
from ha_integration import HAClient
from ingress_server import make_ingress_app
from oauth_flow import OAuthFlow
from pantrist_session import PantristSession
from service_server import make_service_app

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("pantrist_addon")

CONFIG_PATH = "/data/options.json"
INGRESS_PORT = 8100
SERVICE_PORT = 8099


@dataclass
class AddonState:
    socket_url: str
    expiry_warning_days: int
    custom_ha_url: str
    ha_client: HAClient
    session: PantristSession
    oauth_flow: OAuthFlow = field(default_factory=OAuthFlow)
    _list_name_cache: dict = field(default_factory=dict)

    def get_credentials(self) -> Optional[Credentials]:
        return creds_store.load()

    def save_credentials(self, c: Credentials) -> None:
        creds_store.save(c)

    def clear_credentials(self) -> None:
        creds_store.clear()

    def start_session(self, c: Credentials) -> None:
        # Idempotent: stop a previous session first
        self.session.stop()
        self.session.start(c)
        self._list_name_cache.clear()

    def stop_session(self) -> None:
        self.session.stop()

    def get_list_name(self, list_id: str) -> Optional[str]:
        if list_id in self._list_name_cache:
            return self._list_name_cache[list_id]
        if not self.session.is_running:
            return None
        api = getattr(self.session, "_api", None)
        if api is None:
            return None
        try:
            lists = api.get_lists() or []
        except Exception:
            logger.exception("get_lists failed")
            return None
        for li in lists:
            lid = li.get("uuid") if isinstance(li, dict) else getattr(li, "uuid", None)
            settings = li.get("settings", {}) if isinstance(li, dict) else getattr(li, "settings", {})
            name = settings.get("name") if isinstance(settings, dict) else getattr(settings, "name", None)
            if lid and name:
                self._list_name_cache[lid] = name
        return self._list_name_cache.get(list_id)


def load_config() -> dict:
    with open(CONFIG_PATH) as fh:
        return json.load(fh)


async def main_async() -> None:
    cfg = load_config()
    socket_url = cfg["socket_url"]
    expiry_warning_days = int(cfg.get("expiry_warning_days", 7))
    custom_ha_url = (cfg.get("custom_ha_url") or "").strip()

    ha_client = HAClient()
    session = PantristSession(
        socket_url=socket_url,
        expiry_warning_days=expiry_warning_days,
        ha_client=ha_client,
    )
    state = AddonState(
        socket_url=socket_url,
        expiry_warning_days=expiry_warning_days,
        custom_ha_url=custom_ha_url,
        ha_client=ha_client,
        session=session,
    )

    # Phase 1: always-on servers
    ingress_app = make_ingress_app(state)
    service_app = make_service_app(api_provider=lambda: getattr(session, "_api", None))

    ingress_runner = web.AppRunner(ingress_app)
    await ingress_runner.setup()
    await web.TCPSite(ingress_runner, "0.0.0.0", INGRESS_PORT).start()
    logger.info("Ingress UI listening on port %d", INGRESS_PORT)

    service_runner = web.AppRunner(service_app)
    await service_runner.setup()
    await web.TCPSite(service_runner, "0.0.0.0", SERVICE_PORT).start()
    logger.info("Service server listening on port %d", SERVICE_PORT)

    # Phase 2: start session if credentials already exist
    existing = creds_store.load()
    if existing:
        logger.info("Resuming session from /data/credentials.json")
        try:
            state.start_session(existing)
        except Exception:
            logger.exception("Failed to resume session from existing credentials")
    else:
        logger.info("No credentials yet — waiting for OAuth flow via UI")

    stop_event = asyncio.Event()
    loop = asyncio.get_running_loop()

    def _signal_handler():
        logger.info("Shutting down…")
        stop_event.set()

    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, _signal_handler)

    try:
        await stop_event.wait()
    finally:
        session.stop()
        await ingress_runner.cleanup()
        await service_runner.cleanup()


def main() -> None:
    try:
        asyncio.run(main_async())
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
