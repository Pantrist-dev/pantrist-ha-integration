"""Diagnostics tests."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.pantrist.coordinator import PantristCoordinator, PantristData
from custom_components.pantrist.diagnostics import async_get_config_entry_diagnostics

from .conftest import LIST_ID, LIST_NAME


@pytest.mark.usefixtures("mock_oauth_session", "mock_socketio")
async def test_diagnostics_redact_tokens(
    hass: HomeAssistant,
    config_entry: MockConfigEntry,
    mock_api: MagicMock,
) -> None:
    """Diagnostics payload redacts every token key and surfaces list stats."""
    config_entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    payload = await async_get_config_entry_diagnostics(hass, config_entry)

    redacted = payload["entry"]["data"]["token"]
    assert redacted["access_token"] == "**REDACTED**"
    assert redacted["refresh_token"] == "**REDACTED**"
    assert LIST_ID in payload["lists"]
    assert payload["lists"][LIST_ID]["list_name"] == LIST_NAME
    assert payload["lists"][LIST_ID]["last_update_success"] is True


async def test_diagnostics_handles_missing_runtime_data(
    hass: HomeAssistant,
) -> None:
    """An entry without runtime_data yields an empty `lists` dict instead of crashing."""
    entry = MockConfigEntry(
        domain="pantrist",
        unique_id=LIST_ID,
        title=LIST_NAME,
        data={
            "auth_implementation": "pantrist-ha",
            "token": {"access_token": "tok", "refresh_token": "ref"},
            "list_id": LIST_ID,
        },
    )
    entry.add_to_hass(hass)
    payload = await async_get_config_entry_diagnostics(hass, entry)
    assert payload["lists"] == {}
    assert payload["entry"]["data"]["token"]["access_token"] == "**REDACTED**"


async def test_diagnostics_with_no_coordinator_data(hass: HomeAssistant) -> None:
    """A coordinator that hasn't refreshed yet still produces a sane summary."""
    from custom_components.pantrist.diagnostics import _coordinator_diagnostics

    coord = PantristCoordinator(hass, MagicMock(), MagicMock(), LIST_ID, LIST_NAME)
    # not yet refreshed
    coord.data = None  # type: ignore[assignment]
    diag = _coordinator_diagnostics(coord)
    assert diag["shopping_list_count"] == 0
    assert diag["pantry_count"] == 0
    assert diag["shopping_cart_count"] == 0


async def test_diagnostics_with_data(hass: HomeAssistant) -> None:
    from custom_components.pantrist.diagnostics import _coordinator_diagnostics

    coord = PantristCoordinator(hass, MagicMock(), MagicMock(), LIST_ID, LIST_NAME)
    coord.data = PantristData(
        shopping_list={"items": [{"uuid": "1"}, {"uuid": "2"}]},
        pantry={"items": [{"uuid": "3"}]},
        shopping_cart=[{"uuid": "4"}, {"uuid": "5"}, {"uuid": "6"}],
    )
    diag = _coordinator_diagnostics(coord)
    assert diag["shopping_list_count"] == 2
    assert diag["pantry_count"] == 1
    assert diag["shopping_cart_count"] == 3
