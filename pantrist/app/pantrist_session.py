"""Lifecycle wrapper for the Pantrist data pipeline."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Optional

from credentials import Credentials
from ha_integration import (
    HAClient,
    build_expiring_soon_state,
    build_pantry_state,
    build_shopping_cart_state,
    build_shopping_list_state,
)
from pantrist_api import PantristAPI
from socketio_listener import PantristSocketIOListener
from token_manager import TokenManager

logger = logging.getLogger(__name__)


@dataclass
class PantristSession:
    socket_url: str
    expiry_warning_days: int
    ha_client: HAClient

    _api: Optional[PantristAPI] = field(default=None, init=False)
    _sio: Optional[PantristSocketIOListener] = field(default=None, init=False)
    _token_mgr: Optional[TokenManager] = field(default=None, init=False)
    _list_id: str = field(default="", init=False)

    @property
    def is_running(self) -> bool:
        return self._api is not None

    def start(self, creds: Credentials) -> None:
        if self.is_running:
            logger.debug("PantristSession.start() called while running — no-op")
            return

        self._list_id = creds.list_id
        self._token_mgr = TokenManager(
            refresh_token=creds.refresh_token,
            on_token_updated=self._on_token_updated,
            on_failure=self._on_token_failure,
        )
        self._token_mgr.start()

        self._api = PantristAPI(self._token_mgr.access_token)

        self._fetch_all()

        self._sio = PantristSocketIOListener(
            base_url=self.socket_url,
            token=self._token_mgr.access_token,
            shopping_list_id=self._list_id,
            pantry_list_id=self._list_id,
            on_shopping_updated=lambda lid: self._fetch_all(),
            on_pantry_updated=lambda lid: self._fetch_all(),
            on_shopping_cart_updated=lambda lid: self._fetch_all(),
        )
        self._sio.start()
        logger.info("PantristSession started (list=%s)", self._list_id)

    def stop(self) -> None:
        if not self.is_running:
            return
        if self._sio:
            try:
                self._sio.stop()
            except Exception:
                logger.exception("Error stopping SocketIO listener")
        if self._token_mgr:
            try:
                self._token_mgr.stop()
            except Exception:
                logger.exception("Error stopping TokenManager")
        if self._api:
            try:
                self._api.close()
            except Exception:
                logger.exception("Error closing PantristAPI")
        self._api = None
        self._sio = None
        self._token_mgr = None
        logger.info("PantristSession stopped")

    def _on_token_updated(self, new_token: str) -> None:
        if self._api:
            self._api.update_token(new_token)
        if self._sio:
            self._sio.update_token(new_token)

    def _on_token_failure(self) -> None:
        logger.warning("Token refresh failed permanently — stopping session and notifying HA")
        self.ha_client.post_persistent_notification(
            notification_id="pantrist_reauth",
            title="Pantrist",
            message="Pantrist needs to be reconnected. Open the Pantrist add-on UI and click Reconnect.",
        )
        self.stop()

    def _fetch_all(self) -> None:
        if not self._api:
            return
        try:
            shopping = self._api.get_shopping_list(self._list_id)
            state, attrs = build_shopping_list_state(shopping)
            self.ha_client.set_state("sensor.pantrist_shopping_list", state, attrs)
        except Exception:
            logger.exception("Failed to refresh shopping list")
        try:
            pantry = self._api.get_pantry_list(self._list_id)
            state, attrs = build_pantry_state(pantry)
            self.ha_client.set_state("sensor.pantrist_pantry", state, attrs)
            es_state, es_attrs = build_expiring_soon_state(pantry, self.expiry_warning_days)
            self.ha_client.set_state("sensor.pantrist_expiring_soon", es_state, es_attrs)
        except Exception:
            logger.exception("Failed to refresh pantry")
        try:
            cart = self._api.get_shopping_cart(self._list_id)
            state, attrs = build_shopping_cart_state(cart)
            self.ha_client.set_state("sensor.pantrist_shopping_cart", state, attrs)
        except Exception:
            logger.exception("Failed to refresh shopping cart")
