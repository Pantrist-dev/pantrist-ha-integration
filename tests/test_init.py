"""Integration setup and unload."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest
from homeassistant.config_entries import ConfigEntryState
from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.pantrist.const import DOMAIN

from .conftest import LIST_ID, LIST_NAME


@pytest.mark.usefixtures("enable_custom_integrations", "setup_credentials", "mock_socketio")
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
    coords = hass.data[DOMAIN][config_entry.entry_id]
    assert LIST_ID in coords
    assert coords[LIST_ID].list_name == LIST_NAME

    assert await hass.config_entries.async_unload(config_entry.entry_id)
    await hass.async_block_till_done()
    assert config_entry.state is ConfigEntryState.NOT_LOADED


@pytest.mark.usefixtures("enable_custom_integrations", "setup_credentials", "mock_socketio")
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


@pytest.mark.usefixtures("enable_custom_integrations", "setup_credentials", "mock_socketio")
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

    coords = hass.data[DOMAIN][config_entry.entry_id]
    assert set(coords) == {LIST_ID}
