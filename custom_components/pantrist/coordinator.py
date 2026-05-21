"""Coordinator: REST fetch + Socket.IO push for Pantrist data."""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any

import socketio
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers import issue_registry as ir
from homeassistant.helpers.dispatcher import async_dispatcher_send
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.util import dt as dt_util

from .api import PantristApi, PantristApiError, PantristAuthError
from .const import API_BASE, DOMAIN, SOCKET_NAMESPACE

_LOGGER = logging.getLogger(__name__)

_RECONNECT_BACKOFF_START = 2
_RECONNECT_BACKOFF_MAX = 60

# After this much continuous disconnect time we surface a HA Repair issue —
# the user will see "Pantrist real-time updates haven't been working for X
# minutes" in Settings → System → Repairs.
DISCONNECT_REPAIR_THRESHOLD = timedelta(minutes=5)


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
            # No periodic polling. Socket.IO ``data:updated`` events drive
            # every refresh; on reconnect we trigger a one-shot refresh
            # (see :py:meth:`_sio_connect_and_wait`) to catch up on
            # anything missed while the socket was down.
            update_interval=None,
        )
        self._api = api
        self._list_id = list_id
        self._list_name = list_name
        self._sio: socketio.AsyncClient | None = None
        self._sio_task: asyncio.Task | None = None
        self._stop_sio = asyncio.Event()
        # Tracks when the Socket.IO connection first went down. Set on
        # disconnect, cleared on successful reconnect (in the ``connect``
        # event handler). Drives the disconnect Repair issue.
        self._first_disconnect_at: datetime | None = None

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

        new_data = PantristData(
            shopping_list=shopping or {},
            pantry=pantry or {},
            shopping_cart=cart or [],
        )

        # Notify the ``number`` platform when the pantry inventory shifts so
        # it can spawn / retire per-item entities.
        if self._pantry_item_ids(new_data) != self._pantry_item_ids(self.data):
            from .list_manager import signal_pantry_items_changed  # noqa: PLC0415

            entry = self.config_entry
            if entry is not None:
                async_dispatcher_send(
                    self.hass,
                    signal_pantry_items_changed(entry.entry_id),
                    self._list_id,
                )

        return new_data

    @staticmethod
    def _pantry_item_ids(data: PantristData | None) -> frozenset[str]:
        if data is None:
            return frozenset()
        return frozenset(
            str(item["uuid"])
            for item in (data.pantry or {}).get("items", [])
            if item.get("uuid")
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
        # Tear down any pending Repair issue on shutdown so HA doesn't keep
        # showing a stale "disconnected" warning after the integration is
        # unloaded.
        self._clear_disconnect_issue()

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
                # We're between connection attempts — mark the moment we
                # first lost the socket so the Repair-issue check can decide
                # whether to surface the disconnect to the user.
                if self._first_disconnect_at is None:
                    self._first_disconnect_at = dt_util.utcnow()
                self._maybe_register_disconnect_issue()
                _LOGGER.info("Reconnecting Socket.IO in %d s…", backoff)
                try:
                    await asyncio.wait_for(self._stop_sio.wait(), timeout=backoff)
                except asyncio.TimeoutError:
                    pass
                backoff = min(backoff * 2, _RECONNECT_BACKOFF_MAX)

    def _disconnect_issue_id(self) -> str:
        return f"socket_disconnected_{self._list_id}"

    def _maybe_register_disconnect_issue(self) -> None:
        """Register a Repair if we've been disconnected past the threshold."""
        if self._first_disconnect_at is None:
            return
        elapsed = dt_util.utcnow() - self._first_disconnect_at
        if elapsed < DISCONNECT_REPAIR_THRESHOLD:
            return
        ir.async_create_issue(
            self.hass,
            DOMAIN,
            self._disconnect_issue_id(),
            is_fixable=False,
            is_persistent=False,
            severity=ir.IssueSeverity.WARNING,
            translation_key="socket_disconnected",
            translation_placeholders={
                "list_name": self._list_name or self._list_id,
                "minutes": str(max(1, int(elapsed.total_seconds() // 60))),
            },
        )

    def _clear_disconnect_issue(self) -> None:
        if self._first_disconnect_at is None:
            return
        self._first_disconnect_at = None
        ir.async_delete_issue(
            self.hass, DOMAIN, self._disconnect_issue_id()
        )

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
            # We're back. Clear the disconnect-Repair if one was raised.
            self._clear_disconnect_issue()
            # Catch up after any disconnect window. The integration runs
            # without a periodic poll, so this is the only safety net for
            # events missed while the socket was down.
            await self.async_request_refresh()

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

        @sio.on("list:updated", namespace=SOCKET_NAMESPACE)
        async def on_list_updated(data: dict[str, Any]) -> None:
            """Forward server-side rename / settings change to the list manager."""
            if data.get("listId") != self._list_id:
                return
            block = data.get("data") or {}
            new_name = block.get("name") or (
                block.get("settings") or {}
            ).get("name")
            if not new_name:
                return
            # Local import to keep coordinator.py importable without pulling
            # in list_manager at module load time.
            from .list_manager import signal_list_renamed  # noqa: PLC0415

            entry = self.config_entry
            if entry is None:
                return
            async_dispatcher_send(
                self.hass,
                signal_list_renamed(entry.entry_id),
                (self._list_id, str(new_name)),
            )

        @sio.on("list:deleted", namespace=SOCKET_NAMESPACE)
        async def on_list_deleted(data: dict[str, Any]) -> None:
            """Forward server-side list deletion to the list manager."""
            if data.get("listId") != self._list_id:
                return
            from .list_manager import signal_list_deleted  # noqa: PLC0415

            entry = self.config_entry
            if entry is None:
                return
            async_dispatcher_send(
                self.hass,
                signal_list_deleted(entry.entry_id),
                self._list_id,
            )

        @sio.on("list:added", namespace=SOCKET_NAMESPACE)
        async def on_list_added(payload: dict[str, Any]) -> None:
            """Server pushed a new list to the per-user room.

            Each authenticated socket auto-joins ``user:{uid}`` on the
            server, so we receive ``list:added`` for any list that newly
            belongs to (or has been shared with) the account regardless
            of which list room this particular coordinator is in.
            """
            list_id = payload.get("listId") or payload.get("id")
            if not list_id:
                return
            data = payload.get("data") or {}
            list_obj = dict(data) if isinstance(data, dict) else {}
            list_obj.setdefault("id", list_id)

            entry = self.config_entry
            if entry is None:
                return
            manager = getattr(entry, "runtime_data", None)
            if manager is None:
                return
            manager.handle_remote_add(list_obj)

        @sio.on("list:removed", namespace=SOCKET_NAMESPACE)
        async def on_list_removed(payload: dict[str, Any]) -> None:
            """Server pushed a list-revocation to the per-user room."""
            list_id = payload.get("listId") or payload.get("id")
            if not list_id:
                return
            from .list_manager import signal_list_deleted  # noqa: PLC0415

            entry = self.config_entry
            if entry is None:
                return
            async_dispatcher_send(
                self.hass,
                signal_list_deleted(entry.entry_id),
                str(list_id),
            )

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
