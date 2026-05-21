"""Application credentials platform for Pantrist (PKCE-only)."""

from __future__ import annotations

from homeassistant.components.application_credentials import (
    AuthorizationServer,
    ClientCredential,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.config_entry_oauth2_flow import (
    AbstractOAuth2Implementation,
    LocalOAuth2ImplementationWithPkce,
)

from .const import OAUTH2_AUTHORIZE, OAUTH2_TOKEN


async def async_get_auth_implementation(
    hass: HomeAssistant, auth_domain: str, credential: ClientCredential
) -> AbstractOAuth2Implementation:
    """Return the PKCE-only OAuth2 implementation for Pantrist."""
    return LocalOAuth2ImplementationWithPkce(
        hass,
        auth_domain,
        credential.client_id,
        authorize_url=OAUTH2_AUTHORIZE,
        token_url=OAUTH2_TOKEN,
        # PKCE: no client_secret needed; the empty string keeps the helper happy.
        client_secret="",
    )


async def async_get_authorization_server(hass: HomeAssistant) -> AuthorizationServer:
    """Return the Pantrist authorization server endpoints."""
    return AuthorizationServer(
        authorize_url=OAUTH2_AUTHORIZE,
        token_url=OAUTH2_TOKEN,
    )
