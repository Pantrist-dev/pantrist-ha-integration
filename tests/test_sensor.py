"""Sensor entity smoke tests."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest
from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

from .conftest import LIST_ID


@pytest.mark.usefixtures("enable_custom_integrations", "setup_credentials", "mock_socketio")
async def test_sensors_materialize(
    hass: HomeAssistant,
    config_entry: MockConfigEntry,
    mock_api: MagicMock,
) -> None:
    """After setup the four sensors per list exist with sane state."""
    mock_api.get_shopping_list = AsyncMock(
        return_value={
            "listId": LIST_ID,
            "items": [{"uuid": "i1", "name": "Milk", "amount": 1, "unitId": "L"}],
        }
    )
    mock_api.get_pantry_list = AsyncMock(
        return_value={"listId": LIST_ID, "items": []}
    )
    mock_api.get_shopping_cart = AsyncMock(return_value=[])

    config_entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    # Look up entities by their unique IDs (entity_id depends on device name).
    registry = hass.data["entity_registry"]  # type: ignore[index]
    unique_ids = {entry.unique_id for entry in registry.entities.values()}
    assert f"{LIST_ID}_shopping_list" in unique_ids
    assert f"{LIST_ID}_pantry" in unique_ids
    assert f"{LIST_ID}_expiring_soon" in unique_ids
    assert f"{LIST_ID}_shopping_cart" in unique_ids
