"""Shared test fixtures for the Pantrist integration."""

from __future__ import annotations

import time
from collections.abc import Generator
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from homeassistant.components.application_credentials import (
    ClientCredential,
    async_import_client_credential,
)
from homeassistant.core import HomeAssistant
from homeassistant.setup import async_setup_component
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.pantrist.const import CONF_LIST_ID, DOMAIN

CLIENT_ID = "pantrist-ha"
LIST_ID = "00000000-0000-4000-8000-000000000001"
LIST_NAME = "Home"


@pytest.fixture
def enable_custom_integrations(enable_custom_integrations):  # noqa: PT004
    """Hand the standard custom-integrations fixture forward unchanged."""
    yield


@pytest.fixture
async def setup_credentials(hass: HomeAssistant) -> None:
    """Register Pantrist application credentials."""
    assert await async_setup_component(hass, "application_credentials", {})
    await async_import_client_credential(
        hass,
        DOMAIN,
        ClientCredential(CLIENT_ID, ""),
        "pantrist-ha",
    )


@pytest.fixture
def expires_at() -> float:
    """Future timestamp for token expiry."""
    return time.time() + 3600


@pytest.fixture
def config_entry(expires_at: float) -> MockConfigEntry:
    """A pre-configured Pantrist entry as if OAuth already succeeded."""
    return MockConfigEntry(
        domain=DOMAIN,
        unique_id=LIST_ID,
        title=LIST_NAME,
        data={
            "auth_implementation": "pantrist-ha",
            "token": {
                "access_token": "test-access-token",
                "refresh_token": "test-refresh-token",
                "token_type": "Bearer",
                "expires_in": 3600,
                "expires_at": expires_at,
                "list_id": LIST_ID,
            },
            CONF_LIST_ID: LIST_ID,
        },
    )


@pytest.fixture
def mock_api() -> Generator[MagicMock, None, None]:
    """Patch PantristApi so tests don't hit the network."""
    with patch(
        "custom_components.pantrist.PantristApi", autospec=True
    ) as api_cls:
        api = api_cls.return_value
        api.get_lists = AsyncMock(
            return_value=[
                {"id": LIST_ID, "name": LIST_NAME, "settings": {"name": LIST_NAME}}
            ]
        )
        api.get_shopping_list = AsyncMock(
            return_value={"listId": LIST_ID, "items": []}
        )
        api.get_pantry_list = AsyncMock(
            return_value={"listId": LIST_ID, "items": []}
        )
        api.get_shopping_cart = AsyncMock(return_value=[])
        api.add_to_shopping_list_by_name = AsyncMock(return_value={})
        api.add_to_shopping_list_by_barcode = AsyncMock(return_value={})
        api.check_shopping_list_item = AsyncMock(return_value=None)
        api.delete_shopping_list_item = AsyncMock(return_value=None)
        api.add_to_pantry_by_name = AsyncMock(return_value={})
        api.delete_pantry_item = AsyncMock(return_value=None)
        api.change_pantry_item_amount = AsyncMock(return_value={})
        api.lookup_barcode = AsyncMock(return_value=None)
        yield api


@pytest.fixture
def mock_socketio() -> Generator[MagicMock, None, None]:
    """Skip the actual Socket.IO connection in tests."""
    with patch(
        "custom_components.pantrist.coordinator.PantristCoordinator.async_start_socketio",
        new=AsyncMock(),
    ), patch(
        "custom_components.pantrist.coordinator.PantristCoordinator.async_stop_socketio",
        new=AsyncMock(),
    ):
        yield
