"""Per-list coordinator owner with periodic add/remove reconciliation.

One ``PantristListManager`` per config entry. Stored on
``entry.runtime_data`` and exposed as a read-only mapping
(``manager[list_id]``, ``manager.values()`` …) so platforms iterate it
the same way they iterated the old dict.

On top of that the manager schedules a periodic API check that:

* spawns a fresh ``PantristCoordinator`` + signals platforms whenever a
  new list appears in the Pantrist account (Gold: dynamic-devices), and
* stops the coordinator and removes the HA device whenever a list
  disappears (Gold: stale-devices).
"""

from __future__ import annotations

from collections.abc import Iterator, KeysView, ValuesView
from datetime import datetime, timedelta
import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.dispatcher import (
    async_dispatcher_connect,
    async_dispatcher_send,
)
from homeassistant.helpers.event import async_track_time_interval

from .api import PantristApi, PantristApiError, PantristAuthError
from .const import CONF_LIST_ID, DOMAIN
from .coordinator import PantristCoordinator

_LOGGER = logging.getLogger(__name__)

# Slow safety-net reconcile. With ``list:added`` / ``list:removed`` /
# ``list:updated`` / ``list:deleted`` all push-driven over the per-user
# socket room, this is only here to recover from missed events while the
# socket was disconnected.
LIST_RECONCILE_INTERVAL = timedelta(hours=1)


@callback
def signal_new_list(entry_id: str) -> str:
    """Dispatcher signal fired when a previously-unseen list shows up."""
    return f"pantrist_new_list_{entry_id}"


@callback
def signal_list_deleted(entry_id: str) -> str:
    """Dispatcher signal fired when a list is removed server-side."""
    return f"pantrist_list_deleted_{entry_id}"


@callback
def signal_list_renamed(entry_id: str) -> str:
    """Dispatcher signal fired when a list's name changes server-side.

    Payload: ``(list_id, new_name)``.
    """
    return f"pantrist_list_renamed_{entry_id}"


@callback
def signal_pantry_items_changed(entry_id: str) -> str:
    """Dispatcher signal fired when a list's pantry inventory shifts.

    Lets the ``number`` platform reconcile per-item entities against the
    current pantry contents.

    Payload: ``list_id``.
    """
    return f"pantrist_pantry_items_changed_{entry_id}"


class PantristListManager:
    """Per-entry owner of the live coordinator set + reconcile loop."""

    def __init__(
        self, hass: HomeAssistant, entry: ConfigEntry, api: PantristApi
    ) -> None:
        self._hass = hass
        self._entry = entry
        self._api = api
        self._coordinators: dict[str, PantristCoordinator] = {}
        self._unsub_interval: Any | None = None
        self._unsub_signals: list[Any] = []
        # Old entries pin themselves to a single list — preserve that
        # behaviour so a legacy single-list user doesn't suddenly see every
        # list in their account materialise.
        self._legacy_list_id: str | None = (
            entry.data.get(CONF_LIST_ID)
            or (entry.data.get("token") or {}).get("list_id")
        )

    # ------------------------------------------------------------------
    # Mapping interface — drop-in for the old dict[str, PantristCoordinator]
    # ------------------------------------------------------------------

    def __getitem__(self, key: str) -> PantristCoordinator:
        return self._coordinators[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self._coordinators)

    def __contains__(self, key: object) -> bool:
        return key in self._coordinators

    def __len__(self) -> int:
        return len(self._coordinators)

    def values(self) -> ValuesView[PantristCoordinator]:
        return self._coordinators.values()

    def keys(self) -> KeysView[str]:
        return self._coordinators.keys()

    def items(self) -> Any:
        return self._coordinators.items()

    @property
    def api(self) -> PantristApi:
        return self._api

    @property
    def coordinators(self) -> dict[str, PantristCoordinator]:
        return self._coordinators

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    async def async_initial_setup(self) -> None:
        """Enumerate lists, build coordinators, start the reconcile loop.

        Raises:
            ConfigEntryAuthFailed: on 401 — HA will trigger the reauth flow.
            PantristApiError: on any other API failure during the initial
                fetch. The caller turns that into a setup-retry.
        """
        try:
            lists = await self._api.get_lists()
        except PantristAuthError as err:
            raise ConfigEntryAuthFailed(
                "Pantrist auth failed listing lists"
            ) from err

        try:
            await self._apply(lists, fire_signals=False)
        except Exception:
            # Partial setup leaks coordinators / Socket.IO tasks; clean up.
            await self.async_shutdown()
            raise

        if not self._coordinators:
            raise PantristApiError(
                "Pantrist account has no usable lists yet"
            )

        self._unsub_interval = async_track_time_interval(
            self._hass, self._on_interval, LIST_RECONCILE_INTERVAL
        )

        # Socket-driven rename + delete propagate via dispatcher signals
        # fired from each coordinator's socket loop.
        self._unsub_signals.append(
            async_dispatcher_connect(
                self._hass,
                signal_list_deleted(self._entry.entry_id),
                self._handle_remote_delete,
            )
        )
        self._unsub_signals.append(
            async_dispatcher_connect(
                self._hass,
                signal_list_renamed(self._entry.entry_id),
                self._handle_remote_rename,
            )
        )

    async def async_shutdown(self) -> None:
        """Stop the reconcile loop, dispatcher subscriptions, and coordinators."""
        if self._unsub_interval is not None:
            self._unsub_interval()
            self._unsub_interval = None
        for unsub in self._unsub_signals:
            unsub()
        self._unsub_signals.clear()
        for coord in list(self._coordinators.values()):
            await coord.async_stop_socketio()
        self._coordinators.clear()
        # Release the shared httpx client (and its connection pool) we built
        # for this entry's API wrapper.
        await self._api.async_close()

    async def _on_interval(self, _now: datetime) -> None:
        await self.async_reconcile()

    async def async_reconcile(self) -> None:
        """Pull the current list inventory and apply add/remove diffs.

        Network / auth errors are *swallowed* here — the coordinator's
        own poll surfaces backend availability through entity state; we
        don't want a transient reconcile failure to bubble up as a
        config-entry error and tear everything down.
        """
        try:
            lists = await self._api.get_lists()
        except (PantristApiError, PantristAuthError) as err:
            _LOGGER.debug("Skipping list reconcile: %s", err)
            return
        await self._apply(lists, fire_signals=True)

    async def _apply(
        self, lists: list[dict[str, Any]], fire_signals: bool
    ) -> None:
        """Materialise ``lists`` against the current coordinator set."""
        if self._legacy_list_id:
            lists = [
                li
                for li in lists
                if (li.get("id") or li.get("uuid")) == self._legacy_list_id
            ]

        seen_ids: set[str] = set()
        new_ids: list[str] = []

        for list_obj in lists:
            list_id = list_obj.get("id") or list_obj.get("uuid")
            if not list_id:
                continue
            seen_ids.add(list_id)
            list_name = list_obj.get("name")
            if not list_name:
                settings = list_obj.get("settings") or {}
                if isinstance(settings, dict):
                    list_name = settings.get("name")

            if list_id in self._coordinators:
                self._coordinators[list_id].update_list_name(list_name)
                continue

            coord = PantristCoordinator(
                self._hass, self._entry, self._api, list_id, list_name
            )
            await coord.async_config_entry_first_refresh()
            await coord.async_start_socketio()
            self._coordinators[list_id] = coord
            new_ids.append(list_id)

        gone = [lid for lid in self._coordinators if lid not in seen_ids]
        for list_id in gone:
            coord = self._coordinators.pop(list_id)
            await coord.async_stop_socketio()
            self._remove_device(list_id)

        if fire_signals:
            for list_id in new_ids:
                async_dispatcher_send(
                    self._hass,
                    signal_new_list(self._entry.entry_id),
                    list_id,
                )

    def _remove_device(self, list_id: str) -> None:
        """Drop the HA device for a vanished list — cascades to entities."""
        registry = dr.async_get(self._hass)
        device = registry.async_get_device(identifiers={(DOMAIN, list_id)})
        if device is not None:
            registry.async_remove_device(device.id)

    # ------------------------------------------------------------------
    # Socket-driven lifecycle
    # ------------------------------------------------------------------

    @callback
    def _handle_remote_delete(self, list_id: str) -> None:
        """Coordinator heard ``list:deleted`` or ``list:removed``."""
        if list_id not in self._coordinators:
            return
        self._hass.async_create_task(self._remove_list(list_id))

    @callback
    def handle_remote_add(self, list_obj: dict[str, Any]) -> None:
        """Coordinator heard ``list:added`` on the per-user socket room.

        Spawns a fresh coordinator + signals every platform's
        ``async_add_entities`` callback in the same way the reconcile loop
        would. Idempotent against retried emissions.
        """
        list_id = list_obj.get("id") or list_obj.get("uuid")
        if not list_id:
            return
        if self._legacy_list_id and list_id != self._legacy_list_id:
            # A legacy single-list entry must never silently pick up a
            # second list the user didn't opt into.
            return
        if list_id in self._coordinators:
            return
        self._hass.async_create_task(self._spawn_list(list_obj))

    async def _spawn_list(self, list_obj: dict[str, Any]) -> None:
        list_id = str(list_obj.get("id") or list_obj.get("uuid"))
        list_name = list_obj.get("name")
        if not list_name:
            settings = list_obj.get("settings") or {}
            if isinstance(settings, dict):
                list_name = settings.get("name")

        coord = PantristCoordinator(
            self._hass, self._entry, self._api, list_id, list_name
        )
        try:
            await coord.async_config_entry_first_refresh()
        except Exception:  # noqa: BLE001
            _LOGGER.exception("Could not refresh new list %s", list_id)
            return
        await coord.async_start_socketio()
        self._coordinators[list_id] = coord
        async_dispatcher_send(
            self._hass,
            signal_new_list(self._entry.entry_id),
            list_id,
        )

    async def _remove_list(self, list_id: str) -> None:
        coord = self._coordinators.pop(list_id, None)
        if coord is not None:
            await coord.async_stop_socketio()
        self._remove_device(list_id)

    @callback
    def _handle_remote_rename(self, payload: tuple[str, str]) -> None:
        """Coordinator heard ``list:updated`` carrying a new name."""
        list_id, new_name = payload
        coord = self._coordinators.get(list_id)
        if coord is None or not new_name or coord.list_name == new_name:
            return
        coord.update_list_name(new_name)
        # Push the rename into the device registry so the HA UI updates
        # without waiting for the entity platform to re-register.
        registry = dr.async_get(self._hass)
        device = registry.async_get_device(identifiers={(DOMAIN, list_id)})
        if device is not None:
            registry.async_update_device(device.id, name=new_name)
