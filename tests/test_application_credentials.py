"""Application credentials platform tests."""

from __future__ import annotations

from unittest.mock import MagicMock

from homeassistant.components.application_credentials import ClientCredential
from homeassistant.core import HomeAssistant
from homeassistant.helpers.config_entry_oauth2_flow import (
    LocalOAuth2ImplementationWithPkce,
)

from custom_components.pantrist.application_credentials import (
    async_get_auth_implementation,
    async_get_authorization_server,
)
from custom_components.pantrist.const import (
    CLIENT_ID,
    OAUTH2_AUTHORIZE,
    OAUTH2_TOKEN,
)


async def test_auth_implementation_returns_pkce(hass: HomeAssistant) -> None:
    """Pantrist is PKCE-only — secret stays empty even if the user typed one."""
    impl = await async_get_auth_implementation(
        hass,
        "pantrist-ha",
        ClientCredential(client_id=CLIENT_ID, client_secret="unused"),
    )
    assert isinstance(impl, LocalOAuth2ImplementationWithPkce)
    assert impl.authorize_url == OAUTH2_AUTHORIZE
    assert impl.token_url == OAUTH2_TOKEN


async def test_authorization_server_urls(hass: HomeAssistant) -> None:
    """The authorization-server descriptor advertises the Pantrist OAuth endpoints."""
    server = await async_get_authorization_server(hass)
    assert server.authorize_url == OAUTH2_AUTHORIZE
    assert server.token_url == OAUTH2_TOKEN
