"""List manager — dynamic and stale device handling."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.pantrist.api import PantristApiError, PantristAuthError
from custom_components.pantrist.const import DOMAIN
from custom_components.pantrist.coordinator import PantristCoordinator
from custom_components.pantrist.list_manager import (
    PantristListManager,
    signal_new_list,
)

from .conftest import LIST_ID, LIST_NAME


@pytest.fixture(autouse=True)
def _bypass_first_refresh_state_guard():
    """``async_config_entry_first_refresh`` insists the entry is in setup state,
    which we deliberately bypass when unit-testing the manager directly.
    Route the call through the unguarded ``async_refresh`` instead.
    """
    with patch.object(
        PantristCoordinator,
        "async_config_entry_first_refresh",
        new=PantristCoordinator.async_refresh,
    ):
        yield


@pytest.fixture
def manager_entry(expires_at: float) -> MockConfigEntry:
    """A fresh entry (no legacy list_id) so the manager sees every list."""
    return MockConfigEntry(
        domain=DOMAIN,
        unique_id="account-1",
        title="Pantrist",
        data={
            "auth_implementation": "pantrist-ha",
            "token": {
                "access_token": "tok",
                "refresh_token": "ref",
                "expires_at": expires_at,
                # NB: deliberately no list_id, so manager runs in multi-list mode.
            },
        },
    )


@pytest.mark.usefixtures("mock_oauth_session", "mock_socketio")
async def test_initial_setup_aborts_when_no_lists(
    hass: HomeAssistant, manager_entry: MockConfigEntry, mock_api: MagicMock
) -> None:
    """An empty account → PantristApiError so the entry setup returns False."""
    mock_api.get_lists = AsyncMock(return_value=[])
    manager = PantristListManager(hass, manager_entry, mock_api)
    with pytest.raises(PantristApiError):
        await manager.async_initial_setup()


@pytest.mark.usefixtures("mock_oauth_session", "mock_socketio")
async def test_initial_setup_translates_auth_error(
    hass: HomeAssistant, manager_entry: MockConfigEntry, mock_api: MagicMock
) -> None:
    """401 during enumeration triggers ConfigEntryAuthFailed."""
    mock_api.get_lists = AsyncMock(side_effect=PantristAuthError("401"))
    manager = PantristListManager(hass, manager_entry, mock_api)
    with pytest.raises(ConfigEntryAuthFailed):
        await manager.async_initial_setup()


@pytest.mark.usefixtures("mock_oauth_session", "mock_socketio")
async def test_reconcile_fires_signal_on_new_list(
    hass: HomeAssistant, manager_entry: MockConfigEntry, mock_api: MagicMock
) -> None:
    """A list appearing later fires signal_new_list with its UUID."""
    manager_entry.add_to_hass(hass)
    new_list_id = "22222222-2222-4222-8222-222222222222"

    # Initial inventory: one list.
    mock_api.get_lists = AsyncMock(
        return_value=[{"id": LIST_ID, "name": LIST_NAME}]
    )
    manager = PantristListManager(hass, manager_entry, mock_api)
    await manager.async_initial_setup()
    assert set(manager) == {LIST_ID}

    received: list[str] = []
    unsub = async_dispatcher_connect(
        hass, signal_new_list(manager_entry.entry_id), received.append
    )

    # Second poll: a new list shows up.
    mock_api.get_lists = AsyncMock(
        return_value=[
            {"id": LIST_ID, "name": LIST_NAME},
            {"id": new_list_id, "name": "Second"},
        ]
    )
    await manager.async_reconcile()
    await hass.async_block_till_done()
    unsub()

    assert set(manager) == {LIST_ID, new_list_id}
    assert received == [new_list_id]
    await manager.async_shutdown()


@pytest.mark.usefixtures("mock_oauth_session", "mock_socketio")
async def test_reconcile_removes_device_for_vanished_list(
    hass: HomeAssistant, manager_entry: MockConfigEntry, mock_api: MagicMock
) -> None:
    """Lists that disappear server-side are dropped + their HA device removed."""
    manager_entry.add_to_hass(hass)
    second_id = "22222222-2222-4222-8222-222222222222"

    mock_api.get_lists = AsyncMock(
        return_value=[
            {"id": LIST_ID, "name": LIST_NAME},
            {"id": second_id, "name": "Second"},
        ]
    )
    manager = PantristListManager(hass, manager_entry, mock_api)
    await manager.async_initial_setup()

    # Pre-create the device for the second list so we can confirm removal.
    registry = dr.async_get(hass)
    device = registry.async_get_or_create(
        config_entry_id=manager_entry.entry_id,
        identifiers={(DOMAIN, second_id)},
    )
    assert registry.async_get_device(identifiers={(DOMAIN, second_id)}) is not None

    # Second poll: second list is gone.
    mock_api.get_lists = AsyncMock(
        return_value=[{"id": LIST_ID, "name": LIST_NAME}]
    )
    await manager.async_reconcile()

    assert set(manager) == {LIST_ID}
    assert registry.async_get_device(identifiers={(DOMAIN, second_id)}) is None
    await manager.async_shutdown()


@pytest.mark.usefixtures("mock_oauth_session", "mock_socketio")
async def test_reconcile_swallows_api_errors(
    hass: HomeAssistant, manager_entry: MockConfigEntry, mock_api: MagicMock
) -> None:
    """A transient reconcile failure must not propagate."""
    manager_entry.add_to_hass(hass)
    mock_api.get_lists = AsyncMock(
        return_value=[{"id": LIST_ID, "name": LIST_NAME}]
    )
    manager = PantristListManager(hass, manager_entry, mock_api)
    await manager.async_initial_setup()

    mock_api.get_lists = AsyncMock(side_effect=PantristApiError("503"))
    # Should not raise.
    await manager.async_reconcile()
    # And shouldn't have dropped any coordinator.
    assert set(manager) == {LIST_ID}
    await manager.async_shutdown()


@pytest.mark.usefixtures("mock_oauth_session", "mock_socketio")
async def test_reconcile_updates_renamed_list(
    hass: HomeAssistant, manager_entry: MockConfigEntry, mock_api: MagicMock
) -> None:
    """Rename in Pantrist propagates to the coordinator's cached name."""
    manager_entry.add_to_hass(hass)
    mock_api.get_lists = AsyncMock(
        return_value=[{"id": LIST_ID, "name": "Old"}]
    )
    manager = PantristListManager(hass, manager_entry, mock_api)
    await manager.async_initial_setup()
    assert manager[LIST_ID].list_name == "Old"

    mock_api.get_lists = AsyncMock(
        return_value=[{"id": LIST_ID, "name": "New"}]
    )
    await manager.async_reconcile()
    assert manager[LIST_ID].list_name == "New"
    await manager.async_shutdown()


@pytest.mark.usefixtures("mock_oauth_session", "mock_socketio")
async def test_legacy_entry_filters_to_single_list(
    hass: HomeAssistant, config_entry: MockConfigEntry, mock_api: MagicMock
) -> None:
    """Entries from the single-list era only ever expose the pinned list."""
    config_entry.add_to_hass(hass)
    other = "33333333-3333-4333-8333-333333333333"
    mock_api.get_lists = AsyncMock(
        return_value=[
            {"id": LIST_ID, "name": LIST_NAME},
            {"id": other, "name": "Other"},
        ]
    )
    manager = PantristListManager(hass, config_entry, mock_api)
    await manager.async_initial_setup()
    assert set(manager) == {LIST_ID}

    # Even if a new list appears, the legacy entry doesn't pick it up.
    mock_api.get_lists = AsyncMock(
        return_value=[
            {"id": LIST_ID, "name": LIST_NAME},
            {"id": other, "name": "Other"},
            {"id": "44444444-4444-4444-8444-444444444444", "name": "Third"},
        ]
    )
    await manager.async_reconcile()
    assert set(manager) == {LIST_ID}
    await manager.async_shutdown()


@pytest.mark.usefixtures("mock_oauth_session", "mock_socketio")
async def test_manager_mapping_interface(
    hass: HomeAssistant, manager_entry: MockConfigEntry, mock_api: MagicMock
) -> None:
    """PantristListManager behaves like a read-only mapping."""
    manager_entry.add_to_hass(hass)
    mock_api.get_lists = AsyncMock(
        return_value=[{"id": LIST_ID, "name": LIST_NAME}]
    )
    manager = PantristListManager(hass, manager_entry, mock_api)
    await manager.async_initial_setup()

    assert LIST_ID in manager
    assert len(manager) == 1
    assert list(manager) == [LIST_ID]
    assert list(manager.keys()) == [LIST_ID]
    assert manager[LIST_ID].list_name == LIST_NAME
    assert dict(manager.items()) == {LIST_ID: manager[LIST_ID]}
    assert manager.api is mock_api
    assert LIST_ID in manager.coordinators
    await manager.async_shutdown()


@pytest.mark.usefixtures("mock_oauth_session", "mock_socketio")
async def test_initial_setup_rolls_back_on_failure(
    hass: HomeAssistant, manager_entry: MockConfigEntry, mock_api: MagicMock
) -> None:
    """If first_refresh fails midway, no coordinators are left behind."""
    manager_entry.add_to_hass(hass)
    mock_api.get_lists = AsyncMock(
        return_value=[
            {"id": LIST_ID, "name": LIST_NAME},
            {"id": "22222222-2222-4222-8222-222222222222", "name": "Second"},
        ]
    )

    manager = PantristListManager(hass, manager_entry, mock_api)
    call_count = 0

    async def _flaky_refresh(self) -> None:
        nonlocal call_count
        call_count += 1
        if call_count == 2:
            raise RuntimeError("boom")

    with patch(
        "custom_components.pantrist.coordinator."
        "PantristCoordinator.async_config_entry_first_refresh",
        new=_flaky_refresh,
    ):
        with pytest.raises(RuntimeError):
            await manager.async_initial_setup()

    assert len(manager) == 0
