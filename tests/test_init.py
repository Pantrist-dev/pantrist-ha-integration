"""Integration setup and unload."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from homeassistant.config_entries import ConfigEntryState
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.pantrist.api import PantristApiError, PantristAuthError

from .conftest import LIST_ID, LIST_NAME


@pytest.mark.usefixtures("mock_oauth_session", "mock_socketio")
async def test_setup_unload(
    hass: HomeAssistant,
    config_entry: MockConfigEntry,
    mock_api: MagicMock,
) -> None:
    """Happy path: an existing entry sets up, sensors materialize, unload cleans up."""
    config_entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    assert config_entry.state is ConfigEntryState.LOADED
    coords = config_entry.runtime_data
    assert LIST_ID in coords
    assert coords[LIST_ID].list_name == LIST_NAME

    assert await hass.config_entries.async_unload(config_entry.entry_id)
    await hass.async_block_till_done()
    assert config_entry.state is ConfigEntryState.NOT_LOADED


@pytest.mark.usefixtures("mock_oauth_session", "mock_socketio")
async def test_setup_aborts_when_account_has_no_lists(
    hass: HomeAssistant,
    config_entry: MockConfigEntry,
    mock_api: MagicMock,
) -> None:
    """The user removed every list in Pantrist after setup — surface a clean failure."""
    mock_api.get_lists = AsyncMock(return_value=[])

    config_entry.add_to_hass(hass)
    assert not await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()
    assert config_entry.state is ConfigEntryState.SETUP_ERROR


@pytest.mark.usefixtures("mock_oauth_session", "mock_socketio")
async def test_setup_filters_to_legacy_list_id(
    hass: HomeAssistant,
    config_entry: MockConfigEntry,
    mock_api: MagicMock,
) -> None:
    """Entries from the single-list era only surface the chosen list."""
    other_id = "11111111-1111-4111-8111-111111111111"
    mock_api.get_lists = AsyncMock(
        return_value=[
            {"id": LIST_ID, "name": LIST_NAME},
            {"id": other_id, "name": "Other"},
        ]
    )

    config_entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    coords = config_entry.runtime_data
    assert set(coords) == {LIST_ID}


@pytest.mark.usefixtures("mock_oauth_session", "mock_socketio")
async def test_setup_fails_when_legacy_list_id_not_in_account(
    hass: HomeAssistant,
    config_entry: MockConfigEntry,
    mock_api: MagicMock,
) -> None:
    """The legacy list_id no longer exists on the Pantrist account → setup error."""
    mock_api.get_lists = AsyncMock(
        return_value=[{"id": "deadbeef-dead-beef-dead-beefdeadbeef", "name": "Other"}]
    )
    config_entry.add_to_hass(hass)
    assert not await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()
    assert config_entry.state is ConfigEntryState.SETUP_ERROR


@pytest.mark.usefixtures("mock_oauth_session", "mock_socketio")
async def test_setup_fails_when_list_enumeration_errors(
    hass: HomeAssistant,
    config_entry: MockConfigEntry,
    mock_api: MagicMock,
) -> None:
    """A generic API error during list enumeration surfaces as a setup error."""
    mock_api.get_lists = AsyncMock(side_effect=PantristApiError("503"))
    config_entry.add_to_hass(hass)
    assert not await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()
    assert config_entry.state is ConfigEntryState.SETUP_ERROR


@pytest.mark.usefixtures("mock_oauth_session", "mock_socketio")
async def test_setup_raises_auth_failed_on_auth_error(
    hass: HomeAssistant,
    config_entry: MockConfigEntry,
    mock_api: MagicMock,
) -> None:
    """A 401 during enumeration triggers reauth via ConfigEntryAuthFailed."""
    mock_api.get_lists = AsyncMock(side_effect=PantristAuthError("401"))
    config_entry.add_to_hass(hass)
    assert not await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()
    assert config_entry.state is ConfigEntryState.SETUP_ERROR


@pytest.mark.usefixtures("mock_oauth_session", "mock_socketio")
async def test_setup_skips_lists_without_id(
    hass: HomeAssistant,
    config_entry: MockConfigEntry,
    mock_api: MagicMock,
) -> None:
    """Lists missing id/uuid are silently skipped."""
    mock_api.get_lists = AsyncMock(
        return_value=[
            {"name": "No ID"},
            {"id": LIST_ID, "settings": {"name": LIST_NAME}},
        ]
    )
    config_entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()
    assert set(config_entry.runtime_data) == {LIST_ID}


async def test_setup_translates_token_refresh_error(hass: HomeAssistant) -> None:
    """A token refresh failure raises ConfigEntryAuthFailed."""
    from custom_components.pantrist import async_setup_entry

    entry = MockConfigEntry(
        domain="pantrist",
        unique_id=LIST_ID,
        data={
            "auth_implementation": "pantrist-ha",
            "token": {"access_token": "x", "list_id": LIST_ID},
        },
    )
    entry.add_to_hass(hass)
    session = MagicMock()
    session.async_ensure_token_valid = AsyncMock(side_effect=RuntimeError("boom"))
    with patch(
        "custom_components.pantrist.config_entry_oauth2_flow.async_get_config_entry_implementation",
        new=AsyncMock(return_value=MagicMock()),
    ), patch(
        "custom_components.pantrist.config_entry_oauth2_flow.OAuth2Session",
        return_value=session,
    ):
        with pytest.raises(ConfigEntryAuthFailed):
            await async_setup_entry(hass, entry)


async def test_unload_handles_missing_runtime_data(hass: HomeAssistant) -> None:
    """Unloading an entry that never finished setup is a no-op (no exception)."""
    from custom_components.pantrist import async_unload_entry

    entry = MockConfigEntry(domain="pantrist", unique_id=LIST_ID)
    entry.add_to_hass(hass)
    # Don't set runtime_data — simulates an entry that failed during setup.
    assert await async_unload_entry(hass, entry)
