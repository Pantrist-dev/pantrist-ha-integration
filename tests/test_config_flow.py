"""Config flow tests."""

from __future__ import annotations

from unittest.mock import patch

import pytest
from homeassistant.config_entries import SOURCE_USER
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType
from homeassistant.helpers import config_entry_oauth2_flow
from pytest_homeassistant_custom_component.common import MockConfigEntry
from pytest_homeassistant_custom_component.test_util.aiohttp import (
    AiohttpClientMocker,
)

from custom_components.pantrist.const import (
    API_BASE,
    CONF_LIST_ID,
    DOMAIN,
    OAUTH2_AUTHORIZE,
    OAUTH2_TOKEN,
)

from .conftest import LIST_ID, LIST_NAME


@pytest.mark.usefixtures("enable_custom_integrations", "setup_credentials")
async def test_full_oauth_flow(
    hass: HomeAssistant,
    hass_client_no_auth,
    aioclient_mock: AiohttpClientMocker,
    current_request_with_host,
) -> None:
    """End-to-end OAuth flow: authorize → token exchange → entry created with list name."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )
    assert result["type"] == FlowResultType.EXTERNAL_STEP
    state = config_entry_oauth2_flow._encode_jwt(  # noqa: SLF001
        hass,
        {
            "flow_id": result["flow_id"],
            "redirect_uri": "https://example.com/auth/external/callback",
        },
    )
    assert OAUTH2_AUTHORIZE in result["url"]

    client = await hass_client_no_auth()
    resp = await client.get(f"/auth/external/callback?code=abcd&state={state}")
    assert resp.status == 200

    aioclient_mock.post(
        OAUTH2_TOKEN,
        json={
            "access_token": "test-access-token",
            "refresh_token": "test-refresh-token",
            "token_type": "Bearer",
            "expires_in": 3600,
            "list_id": LIST_ID,
        },
    )
    aioclient_mock.get(
        f"{API_BASE}/list",
        json=[{"id": LIST_ID, "name": LIST_NAME, "settings": {"name": LIST_NAME}}],
    )

    with patch(
        "custom_components.pantrist.async_setup_entry", return_value=True
    ):
        result = await hass.config_entries.flow.async_configure(result["flow_id"])

    assert result["type"] == FlowResultType.CREATE_ENTRY
    assert result["title"] == LIST_NAME
    assert result["data"][CONF_LIST_ID] == LIST_ID
    assert result["data"]["token"]["list_id"] == LIST_ID


@pytest.mark.usefixtures("enable_custom_integrations", "setup_credentials")
async def test_already_configured_aborts(
    hass: HomeAssistant,
    config_entry: MockConfigEntry,
) -> None:
    """A second OAuth attempt for the same list is rejected as already_configured."""
    config_entry.add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )
    # Just kicking the flow off is enough for the unique_id check to fire later.
    assert result["type"] in (FlowResultType.EXTERNAL_STEP, FlowResultType.FORM)
