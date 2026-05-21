"""Coordinator: REST fetch + Socket.IO push for Pantrist data."""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import timedelta
from typing import Any

import socketio
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import PantristApi, PantristApiError, PantristAuthError
from .const import API_BASE, DOMAIN, SOCKET_NAMESPACE

_LOGGER = logging.getLogger(__name__)

_RECONNECT_BACKOFF_START = 2
_RECONNECT_BACKOFF_MAX = 60


@dataclass
class PantristData:
    """Snapshot of all data driving the Pantrist sensors."""

    shopping_list: dict[str, Any] = field(default_factory=dict)
    pantry: dict[str, Any] = field(default_factory=dict)
    shopping_cart: list[dict[str, Any]] = field(default_factory=list)


class PantristCoordinator(DataUpdateCoordinator[PantristData]):
    """Fetch via REST, push-update via Socket.IO."""

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        api: PantristApi,
        list_id: str,
        list_name: str | None = None,
    ) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_{list_id}",
            config_entry=config_entry,
            # Polling is a safety net; Socket.IO drives most updates.
            update_interval=timedelta(minutes=5),
        )
        self._api = api
        self._list_id = list_id
        self._list_name = list_name
        self._sio: socketio.AsyncClient | None = None
        self._sio_task: asyncio.Task | None = None
        self._stop_sio = asyncio.Event()

    @property
    def list_id(self) -> str:
        return self._list_id

    @property
    def list_name(self) -> str | None:
        """Human-readable list name, e.g. 'Home'. May be None if unknown."""
        return self._list_name

    def update_list_name(self, name: str | None) -> None:
        """Refresh the cached list name (callable when the list is renamed)."""
        self._list_name = name

    @property
    def api(self) -> PantristApi:
        return self._api

    async def _async_update_data(self) -> PantristData:
        """REST poll — also used by Socket.IO push callbacks."""
        try:
            shopping, pantry, cart = await asyncio.gather(
                self._api.get_shopping_list(self._list_id),
                self._api.get_pantry_list(self._list_id),
                self._api.get_shopping_cart(self._list_id),
            )
        except PantristAuthError as err:
            raise ConfigEntryAuthFailed("Pantrist auth failed") from err
        except PantristApiError as err:
            raise UpdateFailed(f"Pantrist API error: {err}") from err

        return PantristData(
            shopping_list=shopping or {},
            pantry=pantry or {},
            shopping_cart=cart or [],
        )

    # ------------------------------------------------------------------
    # Socket.IO
    # ------------------------------------------------------------------

    async def async_start_socketio(self) -> None:
        """Start the Socket.IO listener task."""
        self._stop_sio.clear()
        self._sio_task = self.hass.loop.create_task(self._sio_loop())

    async def async_stop_socketio(self) -> None:
        self._stop_sio.set()
        sio = self._sio
        if sio is not None and sio.connected:
            try:
                await sio.disconnect()
            except Exception:  # noqa: BLE001
                _LOGGER.debug("Socket.IO disconnect raised on stop", exc_info=True)
        if self._sio_task and not self._sio_task.done():
            self._sio_task.cancel()
            try:
                await self._sio_task
            except (asyncio.CancelledError, Exception):  # noqa: BLE001
                pass
        self._sio = None
        self._sio_task = None

    async def _sio_loop(self) -> None:
        backoff = _RECONNECT_BACKOFF_START
        while not self._stop_sio.is_set():
            try:
                await self._sio_connect_and_wait()
                backoff = _RECONNECT_BACKOFF_START
            except asyncio.CancelledError:
                return
            except Exception:  # noqa: BLE001
                _LOGGER.exception("Socket.IO loop error")
            if not self._stop_sio.is_set():
                _LOGGER.info("Reconnecting Socket.IO in %d s…", backoff)
                try:
                    await asyncio.wait_for(self._stop_sio.wait(), timeout=backoff)
                except asyncio.TimeoutError:
                    pass
                backoff = min(backoff * 2, _RECONNECT_BACKOFF_MAX)

    async def _sio_connect_and_wait(self) -> None:
        await self._api._session.async_ensure_token_valid()  # noqa: SLF001
        token = self._api._session.token["access_token"]  # noqa: SLF001

        sio = socketio.AsyncClient(logger=False, engineio_logger=False)
        self._sio = sio

        @sio.event(namespace=SOCKET_NAMESPACE)
        async def connect() -> None:
            _LOGGER.info("Socket.IO connected to %s%s", API_BASE, SOCKET_NAMESPACE)
            await sio.emit(
                "joinList",
                {"listId": self._list_id},
                namespace=SOCKET_NAMESPACE,
            )

        @sio.event(namespace=SOCKET_NAMESPACE)
        async def disconnect() -> None:
            _LOGGER.info("Socket.IO disconnected")

        @sio.on("data:updated", namespace=SOCKET_NAMESPACE)
        async def on_data_updated(data: dict[str, Any]) -> None:
            list_id = data.get("listId")
            if list_id != self._list_id:
                return
            _LOGGER.debug(
                "data:updated for collection=%s listId=%s — refetching",
                data.get("collection"),
                list_id,
            )
            await self.async_request_refresh()

        await sio.connect(
            API_BASE,
            namespaces=[SOCKET_NAMESPACE],
            auth={"token": token},
            transports=["websocket"],
        )
        try:
            await sio.wait()
        finally:
            if sio.connected:
                try:
                    await sio.disconnect()
                except Exception:  # noqa: BLE001
                    pass
            if self._sio is sio:
                self._sio = None
