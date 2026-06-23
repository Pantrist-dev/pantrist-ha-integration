"""Coordinator unit tests."""

from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
import socketio
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import UpdateFailed

from custom_components.pantrist.api import PantristApiError, PantristAuthError
from custom_components.pantrist.coordinator import PantristCoordinator, PantristData

from .conftest import LIST_ID, LIST_NAME


def _build(hass: HomeAssistant, api: MagicMock | None = None) -> PantristCoordinator:
    return PantristCoordinator(
        hass, MagicMock(), api or MagicMock(), LIST_ID, LIST_NAME
    )


async def test_update_data_aggregates_three_endpoints(hass: HomeAssistant) -> None:
    """A normal refresh pulls shopping/pantry/cart in parallel and packages the snapshot."""
    api = MagicMock()
    api.get_shopping_list = AsyncMock(return_value={"items": [{"uuid": "s"}]})
    api.get_pantry_list = AsyncMock(return_value={"items": [{"uuid": "p"}]})
    api.get_shopping_cart = AsyncMock(return_value=[{"uuid": "c"}])

    coord = _build(hass, api)
    data = await coord._async_update_data()
    assert isinstance(data, PantristData)
    assert data.shopping_list["items"][0]["uuid"] == "s"
    assert data.pantry["items"][0]["uuid"] == "p"
    assert data.shopping_cart[0]["uuid"] == "c"


async def test_update_data_translates_auth_error(hass: HomeAssistant) -> None:
    """A 401 surfaces as ConfigEntryAuthFailed so HA triggers reauth."""
    api = MagicMock()
    api.get_shopping_list = AsyncMock(side_effect=PantristAuthError("401"))
    api.get_pantry_list = AsyncMock(return_value={"items": []})
    api.get_shopping_cart = AsyncMock(return_value=[])

    coord = _build(hass, api)
    with pytest.raises(ConfigEntryAuthFailed):
        await coord._async_update_data()


async def test_update_data_translates_api_error(hass: HomeAssistant) -> None:
    """A non-auth API error becomes UpdateFailed."""
    api = MagicMock()
    api.get_shopping_list = AsyncMock(side_effect=PantristApiError("503"))
    api.get_pantry_list = AsyncMock(return_value={"items": []})
    api.get_shopping_cart = AsyncMock(return_value=[])

    coord = _build(hass, api)
    with pytest.raises(UpdateFailed):
        await coord._async_update_data()


async def test_update_list_name_setter(hass: HomeAssistant) -> None:
    coord = _build(hass)
    coord.update_list_name("Renamed")
    assert coord.list_name == "Renamed"
    coord.update_list_name(None)
    assert coord.list_name is None


async def test_properties(hass: HomeAssistant) -> None:
    api = MagicMock()
    coord = _build(hass, api)
    assert coord.list_id == LIST_ID
    assert coord.list_name == LIST_NAME
    assert coord.api is api


async def test_stop_socketio_disconnects_open_client(hass: HomeAssistant) -> None:
    """stop disconnects an active client and cancels the loop task."""
    coord = _build(hass)
    sio = MagicMock()
    sio.connected = True
    sio.disconnect = AsyncMock()
    coord._sio = sio

    async def _loop():
        try:
            await asyncio.sleep(99)
        except asyncio.CancelledError:
            raise

    coord._sio_task = hass.loop.create_task(_loop())
    await coord.async_stop_socketio()
    sio.disconnect.assert_awaited_once()
    assert coord._sio is None
    assert coord._sio_task is None


async def test_stop_socketio_swallows_disconnect_errors(hass: HomeAssistant) -> None:
    coord = _build(hass)
    sio = MagicMock()
    sio.connected = True
    sio.disconnect = AsyncMock(side_effect=RuntimeError("boom"))
    coord._sio = sio
    coord._sio_task = None
    await coord.async_stop_socketio()
    assert coord._sio is None


async def test_stop_socketio_noop_when_inactive(hass: HomeAssistant) -> None:
    """Stopping an unstarted coordinator is fine."""
    coord = _build(hass)
    await coord.async_stop_socketio()
    assert coord._sio is None
    assert coord._sio_task is None


async def test_disconnect_repair_below_threshold_is_quiet(
    hass: HomeAssistant,
) -> None:
    """A short disconnect window must NOT raise a Repair issue."""
    from datetime import timedelta
    from homeassistant.helpers import issue_registry as ir
    from homeassistant.util import dt as dt_util

    from custom_components.pantrist.const import DOMAIN

    coord = _build(hass)
    coord._first_disconnect_at = dt_util.utcnow() - timedelta(seconds=30)
    coord._maybe_register_disconnect_issue()
    assert (
        ir.async_get(hass).async_get_issue(DOMAIN, coord._disconnect_issue_id())
        is None
    )


async def test_disconnect_repair_above_threshold_fires(hass: HomeAssistant) -> None:
    """Once we've been down past the threshold a Repair is registered."""
    from datetime import timedelta
    from homeassistant.helpers import issue_registry as ir
    from homeassistant.util import dt as dt_util

    from custom_components.pantrist.const import DOMAIN

    coord = _build(hass)
    coord._first_disconnect_at = dt_util.utcnow() - timedelta(minutes=6)
    coord._maybe_register_disconnect_issue()
    issue = ir.async_get(hass).async_get_issue(
        DOMAIN, coord._disconnect_issue_id()
    )
    assert issue is not None
    assert issue.translation_key == "socket_disconnected"
    # And clearing wipes it.
    coord._clear_disconnect_issue()
    assert (
        ir.async_get(hass).async_get_issue(DOMAIN, coord._disconnect_issue_id())
        is None
    )


async def test_clear_disconnect_issue_noop_when_never_set(
    hass: HomeAssistant,
) -> None:
    """Clearing when no disconnect was tracked is a no-op."""
    coord = _build(hass)
    coord._clear_disconnect_issue()  # must not raise


async def test_sio_loop_retries_then_exits(hass: HomeAssistant) -> None:
    """The loop catches errors, then exits cleanly once stop is signalled."""
    coord = _build(hass)
    calls = 0

    async def _fake_connect():
        nonlocal calls
        calls += 1
        if calls == 1:
            raise RuntimeError("first attempt fails")
        coord._stop_sio.set()

    with patch.object(coord, "_sio_connect_and_wait", new=_fake_connect):
        coord._stop_sio.clear()
        # Patch asyncio.wait_for so the reconnect backoff doesn't actually sleep.
        async def _instant_wait_for(coro, timeout):
            # Cancel the awaited coroutine and return immediately.
            try:
                coro.close()
            except Exception:  # noqa: BLE001
                pass
            raise asyncio.TimeoutError

        with patch("custom_components.pantrist.coordinator.asyncio.wait_for", new=_instant_wait_for):
            await coord._sio_loop()
    assert calls >= 2


async def test_sio_loop_handles_cancellation(hass: HomeAssistant) -> None:
    """A CancelledError inside the loop exits cleanly without re-raising."""
    coord = _build(hass)

    async def _raises_cancel():
        raise asyncio.CancelledError

    with patch.object(coord, "_sio_connect_and_wait", new=_raises_cancel):
        await coord._sio_loop()  # returns without raising


async def test_start_socketio_creates_task(hass: HomeAssistant) -> None:
    coord = _build(hass)
    with patch.object(coord, "_sio_loop", new=AsyncMock()):
        await coord.async_start_socketio()
        assert coord._sio_task is not None
        coord._sio_task.cancel()
        try:
            await coord._sio_task
        except asyncio.CancelledError:
            pass


async def test_sio_connect_and_wait_registers_handlers(hass: HomeAssistant) -> None:
    """_sio_connect_and_wait builds the client, connects, then waits until disconnect."""
    api = MagicMock()
    api._session = MagicMock()
    api._session.async_ensure_token_valid = AsyncMock()
    api._session.token = {"access_token": "tok"}

    coord = _build(hass, api)

    fake_sio = MagicMock()
    fake_sio.connect = AsyncMock()
    fake_sio.wait = AsyncMock()
    fake_sio.disconnect = AsyncMock()
    fake_sio.connected = False
    fake_sio.event = MagicMock(side_effect=lambda **_k: (lambda fn: fn))
    fake_sio.on = MagicMock(side_effect=lambda *_a, **_k: (lambda fn: fn))
    fake_sio.emit = AsyncMock()

    with patch(
        "custom_components.pantrist.coordinator.socketio.AsyncClient",
        return_value=fake_sio,
    ):
        await coord._sio_connect_and_wait()

    fake_sio.connect.assert_awaited_once()
    fake_sio.wait.assert_awaited_once()


async def test_sio_connect_disconnect_swallows_errors(hass: HomeAssistant) -> None:
    """If `wait` returns and the client is still connected, disconnect errors are swallowed."""
    api = MagicMock()
    api._session = MagicMock()
    api._session.async_ensure_token_valid = AsyncMock()
    api._session.token = {"access_token": "tok"}

    coord = _build(hass, api)

    fake_sio = MagicMock()
    fake_sio.connect = AsyncMock()
    fake_sio.wait = AsyncMock()
    fake_sio.disconnect = AsyncMock(side_effect=RuntimeError("boom"))
    fake_sio.connected = True
    fake_sio.event = MagicMock(side_effect=lambda **_k: (lambda fn: fn))
    fake_sio.on = MagicMock(side_effect=lambda *_a, **_k: (lambda fn: fn))
    fake_sio.emit = AsyncMock()

    with patch(
        "custom_components.pantrist.coordinator.socketio.AsyncClient",
        return_value=fake_sio,
    ):
        await coord._sio_connect_and_wait()


async def test_sio_connect_failure_closes_leaked_session(
    hass: HomeAssistant,
) -> None:
    """A failed connect must still close the engineio aiohttp session.

    engineio leaks its ClientSession when the WebSocket connect fails, which
    during a DNS / network outage would accumulate "Unclosed client session"
    errors and destabilise HA. The connect attempt must clean it up.
    """
    api = MagicMock()
    api._session = MagicMock()
    api._session.async_ensure_token_valid = AsyncMock()
    api._session.token = {"access_token": "tok"}

    coord = _build(hass, api)

    http = MagicMock()
    http.closed = False
    http.close = AsyncMock()

    fake_sio = MagicMock()
    fake_sio.connect = AsyncMock(
        side_effect=socketio.exceptions.ConnectionError("Connection error")
    )
    fake_sio.wait = AsyncMock()
    fake_sio.disconnect = AsyncMock()
    fake_sio.connected = False
    fake_sio.eio = MagicMock()
    fake_sio.eio.http = http
    fake_sio.event = MagicMock(side_effect=lambda **_k: (lambda fn: fn))
    fake_sio.on = MagicMock(side_effect=lambda *_a, **_k: (lambda fn: fn))
    fake_sio.emit = AsyncMock()

    with patch(
        "custom_components.pantrist.coordinator.socketio.AsyncClient",
        return_value=fake_sio,
    ):
        with pytest.raises(socketio.exceptions.ConnectionError):
            await coord._sio_connect_and_wait()

    # The leaked session was closed, and we never blocked in wait().
    http.close.assert_awaited_once()
    fake_sio.wait.assert_not_awaited()
    assert coord._sio is None


async def test_sio_event_callbacks_invoked(hass: HomeAssistant) -> None:
    """Trip the registered Socket.IO callbacks to cover their bodies."""
    api = MagicMock()
    api._session = MagicMock()
    api._session.async_ensure_token_valid = AsyncMock()
    api._session.token = {"access_token": "tok"}

    coord = _build(hass, api)

    captured: dict[str, list[Callable[..., Awaitable[None]]]] = {}

    def _event(**_kwargs: Any) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        def deco(fn: Callable[..., Any]) -> Callable[..., Any]:
            captured.setdefault("events", []).append(fn)
            return fn

        return deco

    def _on(
        event_name: str, **_kwargs: Any
    ) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        def deco(fn: Callable[..., Any]) -> Callable[..., Any]:
            captured.setdefault(event_name, []).append(fn)
            return fn

        return deco

    fake_sio = MagicMock()
    fake_sio.connect = AsyncMock()
    fake_sio.wait = AsyncMock()
    fake_sio.disconnect = AsyncMock()
    fake_sio.connected = False
    fake_sio.event = MagicMock(side_effect=_event)
    fake_sio.on = MagicMock(side_effect=_on)
    fake_sio.emit = AsyncMock()

    with patch(
        "custom_components.pantrist.coordinator.socketio.AsyncClient",
        return_value=fake_sio,
    ):
        await coord._sio_connect_and_wait()

    # Trigger the two @sio.event handlers: connect (calls emit) + disconnect.
    connect_cb, disconnect_cb = captured["events"]
    await connect_cb()
    fake_sio.emit.assert_awaited_with(
        "joinList", {"listId": LIST_ID}, namespace="/lists"
    )
    await disconnect_cb()

    # Trigger data:updated with a matching listId (refresh) + mismatched (ignored).
    data_updated_cb = captured["data:updated"][0]
    refresh_mock = AsyncMock()
    coord.async_request_refresh = refresh_mock  # type: ignore[method-assign]
    await data_updated_cb({"listId": LIST_ID, "collection": "shoppingList"})
    refresh_mock.assert_awaited_once()
    await data_updated_cb({"listId": "different", "collection": "x"})
    assert refresh_mock.await_count == 1


async def test_sio_list_lifecycle_callbacks_fire_dispatcher_signals(
    hass: HomeAssistant,
) -> None:
    """The `list:updated` / `list:deleted` handlers dispatch into the manager."""
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.helpers.dispatcher import async_dispatcher_connect
    from pytest_homeassistant_custom_component.common import MockConfigEntry

    from custom_components.pantrist.const import DOMAIN
    from custom_components.pantrist.list_manager import (
        signal_list_deleted,
        signal_list_renamed,
    )

    api = MagicMock()
    api._session = MagicMock()
    api._session.async_ensure_token_valid = AsyncMock()
    api._session.token = {"access_token": "tok"}

    entry = MockConfigEntry(domain=DOMAIN, unique_id=LIST_ID)
    entry.add_to_hass(hass)

    coord = PantristCoordinator(hass, entry, api, LIST_ID, LIST_NAME)

    captured: dict[str, list[Callable[..., Awaitable[None]]]] = {}

    def _event(**_kwargs: Any) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        def deco(fn: Callable[..., Any]) -> Callable[..., Any]:
            captured.setdefault("events", []).append(fn)
            return fn

        return deco

    def _on(
        event_name: str, **_kwargs: Any
    ) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        def deco(fn: Callable[..., Any]) -> Callable[..., Any]:
            captured.setdefault(event_name, []).append(fn)
            return fn

        return deco

    fake_sio = MagicMock()
    fake_sio.connect = AsyncMock()
    fake_sio.wait = AsyncMock()
    fake_sio.disconnect = AsyncMock()
    fake_sio.connected = False
    fake_sio.event = MagicMock(side_effect=_event)
    fake_sio.on = MagicMock(side_effect=_on)
    fake_sio.emit = AsyncMock()

    with patch(
        "custom_components.pantrist.coordinator.socketio.AsyncClient",
        return_value=fake_sio,
    ):
        await coord._sio_connect_and_wait()

    rename_payload: list[tuple[str, str]] = []
    delete_payload: list[str] = []

    # The receivers must be @callback so HA's dispatcher runs them inline on
    # the event loop. Bare ``list.append`` is detected as an Executor job,
    # which runs in a worker thread and races between consecutive sends.
    from homeassistant.core import callback as hass_callback

    @hass_callback
    def _capture_rename(payload: tuple[str, str]) -> None:
        rename_payload.append(payload)

    @hass_callback
    def _capture_delete(payload: str) -> None:
        delete_payload.append(payload)

    unsub_rename = async_dispatcher_connect(
        hass, signal_list_renamed(entry.entry_id), _capture_rename
    )
    unsub_delete = async_dispatcher_connect(
        hass, signal_list_deleted(entry.entry_id), _capture_delete
    )

    list_updated_cb = captured["list:updated"][0]
    list_deleted_cb = captured["list:deleted"][0]

    # Wrong listId → ignored.
    await list_updated_cb({"listId": "other", "data": {"name": "X"}})
    await list_deleted_cb({"listId": "other"})
    await hass.async_block_till_done()
    assert rename_payload == []
    assert delete_payload == []

    # No-name update → ignored.
    await list_updated_cb({"listId": LIST_ID, "data": {}})
    await hass.async_block_till_done()
    assert rename_payload == []

    # name in top-level data.
    await list_updated_cb({"listId": LIST_ID, "data": {"name": "Top"}})
    # name nested in settings.
    await list_updated_cb(
        {"listId": LIST_ID, "data": {"settings": {"name": "Nested"}}}
    )
    await list_deleted_cb({"listId": LIST_ID})
    await hass.async_block_till_done()

    unsub_rename()
    unsub_delete()
    assert rename_payload == [(LIST_ID, "Top"), (LIST_ID, "Nested")]
    assert delete_payload == [LIST_ID]


async def test_sio_user_room_callbacks_fire_dispatcher_signals(
    hass: HomeAssistant,
) -> None:
    """The ``list:added`` / ``list:removed`` handlers route into the manager."""
    from homeassistant.core import callback as hass_callback
    from homeassistant.helpers.dispatcher import async_dispatcher_connect
    from pytest_homeassistant_custom_component.common import MockConfigEntry

    from custom_components.pantrist.const import DOMAIN
    from custom_components.pantrist.list_manager import signal_list_deleted

    api = MagicMock()
    api._session = MagicMock()
    api._session.async_ensure_token_valid = AsyncMock()
    api._session.token = {"access_token": "tok"}

    entry = MockConfigEntry(domain=DOMAIN, unique_id=LIST_ID)
    entry.add_to_hass(hass)

    # Drop in a stub manager so handle_remote_add is observable.
    handled: list[dict[str, Any]] = []

    class _StubManager:
        @hass_callback
        def handle_remote_add(self, payload: dict[str, Any]) -> None:
            handled.append(payload)

    entry.runtime_data = _StubManager()  # type: ignore[assignment]

    coord = PantristCoordinator(hass, entry, api, LIST_ID, LIST_NAME)

    captured: dict[str, list[Callable[..., Awaitable[None]]]] = {}

    def _event(**_kwargs: Any) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        def deco(fn: Callable[..., Any]) -> Callable[..., Any]:
            captured.setdefault("events", []).append(fn)
            return fn

        return deco

    def _on(
        event_name: str, **_kwargs: Any
    ) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        def deco(fn: Callable[..., Any]) -> Callable[..., Any]:
            captured.setdefault(event_name, []).append(fn)
            return fn

        return deco

    fake_sio = MagicMock()
    fake_sio.connect = AsyncMock()
    fake_sio.wait = AsyncMock()
    fake_sio.disconnect = AsyncMock()
    fake_sio.connected = False
    fake_sio.event = MagicMock(side_effect=_event)
    fake_sio.on = MagicMock(side_effect=_on)
    fake_sio.emit = AsyncMock()

    with patch(
        "custom_components.pantrist.coordinator.socketio.AsyncClient",
        return_value=fake_sio,
    ):
        await coord._sio_connect_and_wait()

    removed: list[str] = []

    @hass_callback
    def _capture_removed(payload: str) -> None:
        removed.append(payload)

    unsub_removed = async_dispatcher_connect(
        hass, signal_list_deleted(entry.entry_id), _capture_removed
    )

    list_added_cb = captured["list:added"][0]
    list_removed_cb = captured["list:removed"][0]

    # Payload with no id → silently dropped.
    await list_added_cb({})
    await list_removed_cb({})
    await hass.async_block_till_done()
    assert handled == []
    assert removed == []

    # Real list:added → manager.handle_remote_add called.
    new_id = "77777777-7777-4777-8777-777777777777"
    await list_added_cb({"listId": new_id, "data": {"id": new_id, "name": "X"}})
    await hass.async_block_till_done()
    assert handled[0]["id"] == new_id

    # Payload variant: data is None → coordinator falls back to listId only.
    await list_added_cb({"listId": "abc", "data": None})
    await hass.async_block_till_done()
    assert handled[-1]["id"] == "abc"

    # list:removed dispatches signal_list_deleted with the id.
    await list_removed_cb({"listId": new_id})
    await hass.async_block_till_done()
    unsub_removed()
    assert removed == [new_id]


async def test_sio_user_room_callbacks_ignore_missing_runtime_data(
    hass: HomeAssistant,
) -> None:
    """list:added on a coordinator whose entry has no runtime_data is a no-op."""
    from homeassistant.core import callback as hass_callback
    from pytest_homeassistant_custom_component.common import MockConfigEntry

    from custom_components.pantrist.const import DOMAIN

    api = MagicMock()
    api._session = MagicMock()
    api._session.async_ensure_token_valid = AsyncMock()
    api._session.token = {"access_token": "tok"}

    entry = MockConfigEntry(domain=DOMAIN, unique_id=LIST_ID)
    entry.add_to_hass(hass)
    # Deliberately leave entry.runtime_data unset.

    coord = PantristCoordinator(hass, entry, api, LIST_ID, LIST_NAME)
    captured: dict[str, list[Callable[..., Awaitable[None]]]] = {}

    def _event(**_kwargs: Any) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        def deco(fn: Callable[..., Any]) -> Callable[..., Any]:
            captured.setdefault("events", []).append(fn)
            return fn

        return deco

    def _on(
        event_name: str, **_kwargs: Any
    ) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        def deco(fn: Callable[..., Any]) -> Callable[..., Any]:
            captured.setdefault(event_name, []).append(fn)
            return fn

        return deco

    fake_sio = MagicMock()
    fake_sio.connect = AsyncMock()
    fake_sio.wait = AsyncMock()
    fake_sio.disconnect = AsyncMock()
    fake_sio.connected = False
    fake_sio.event = MagicMock(side_effect=_event)
    fake_sio.on = MagicMock(side_effect=_on)
    fake_sio.emit = AsyncMock()

    with patch(
        "custom_components.pantrist.coordinator.socketio.AsyncClient",
        return_value=fake_sio,
    ):
        await coord._sio_connect_and_wait()

    # Should swallow silently — exercises the ``if manager is None`` guard.
    await captured["list:added"][0](
        {"listId": "x", "data": {"id": "x"}}
    )
    await hass.async_block_till_done()
