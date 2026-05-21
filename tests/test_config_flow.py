"""Config flow tests."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from aiohttp import ClientError
from homeassistant.config_entries import SOURCE_REAUTH, SOURCE_USER
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.pantrist.config_flow import PantristOAuth2FlowHandler
from custom_components.pantrist.const import API_BASE, CONF_LIST_ID, DOMAIN

from .conftest import LIST_ID, LIST_NAME


def _make_flow(hass: HomeAssistant, source: str = SOURCE_USER) -> PantristOAuth2FlowHandler:
    """Construct a flow handler with hass + a minimal context."""
    flow = PantristOAuth2FlowHandler()
    flow.hass = hass
    flow.context = {"source": source}
    # Manually wire `handler` so the unique-id machinery can look up sibling
    # entries via `hass.config_entries.async_entries(self.handler)`.
    flow.init_step = "user"
    flow.handler = DOMAIN
    return flow


async def test_create_entry_uses_list_name_as_title(hass: HomeAssistant) -> None:
    """Happy path: token carries a list_id → entry title is the list name."""
    flow = _make_flow(hass)
    with patch.object(
        PantristOAuth2FlowHandler,
        "_fetch_list_name",
        new=AsyncMock(return_value=LIST_NAME),
    ), patch.object(
        PantristOAuth2FlowHandler, "_test_credentials",
        new=AsyncMock(return_value=None),
    ):
        result = await flow.async_oauth_create_entry(
            {"token": {"access_token": "x", "list_id": LIST_ID}}
        )
    assert result["type"] == FlowResultType.CREATE_ENTRY
    assert result["title"] == LIST_NAME
    assert result["data"][CONF_LIST_ID] == LIST_ID


async def test_create_entry_falls_back_to_uuid_title(hass: HomeAssistant) -> None:
    """If the list-name lookup fails, the title falls back to a UUID stub."""
    flow = _make_flow(hass)
    with patch.object(
        PantristOAuth2FlowHandler,
        "_fetch_list_name",
        new=AsyncMock(return_value=None),
    ), patch.object(
        PantristOAuth2FlowHandler, "_test_credentials",
        new=AsyncMock(return_value=None),
    ):
        result = await flow.async_oauth_create_entry(
            {"token": {"access_token": "x", "list_id": LIST_ID}}
        )
    assert result["type"] == FlowResultType.CREATE_ENTRY
    assert result["title"].startswith("Pantrist (list ")


async def test_create_entry_aborts_without_list_id(hass: HomeAssistant) -> None:
    """A token without a list_id triggers a clean abort."""
    flow = _make_flow(hass)
    result = await flow.async_oauth_create_entry({"token": {"access_token": "x"}})
    assert result["type"] == FlowResultType.ABORT
    assert result["reason"] == "missing_list_id"


async def test_create_entry_aborts_when_credentials_fail(hass: HomeAssistant) -> None:
    """test-before-configure: if the token can't fetch anything, abort."""
    flow = _make_flow(hass)
    with patch.object(
        PantristOAuth2FlowHandler,
        "_test_credentials",
        new=AsyncMock(return_value="cannot_connect"),
    ):
        result = await flow.async_oauth_create_entry(
            {"token": {"access_token": "x", "list_id": LIST_ID}}
        )
    assert result["type"] == FlowResultType.ABORT
    assert result["reason"] == "cannot_connect"


async def test_already_configured_aborts(hass: HomeAssistant) -> None:
    """Re-running OAuth for an already-configured list aborts via unique_id."""
    from homeassistant.data_entry_flow import AbortFlow

    existing = MockConfigEntry(
        domain=DOMAIN,
        unique_id=LIST_ID,
        data={CONF_LIST_ID: LIST_ID, "token": {"list_id": LIST_ID}},
    )
    existing.add_to_hass(hass)

    flow = _make_flow(hass)
    with patch.object(
        PantristOAuth2FlowHandler,
        "_fetch_list_name",
        new=AsyncMock(return_value=LIST_NAME),
    ), patch.object(
        PantristOAuth2FlowHandler, "_test_credentials",
        new=AsyncMock(return_value=None),
    ):
        with pytest.raises(AbortFlow) as excinfo:
            await flow.async_oauth_create_entry(
                {"token": {"access_token": "x", "list_id": LIST_ID}}
            )
    assert excinfo.value.reason == "already_configured"


async def test_reauth_updates_entry(hass: HomeAssistant) -> None:
    """A reauth flow with a matching list_id updates and reloads the existing entry."""
    existing = MockConfigEntry(
        domain=DOMAIN,
        unique_id=LIST_ID,
        data={CONF_LIST_ID: LIST_ID, "token": {"list_id": LIST_ID}},
    )
    existing.add_to_hass(hass)

    flow = _make_flow(hass, source=SOURCE_REAUTH)
    flow.context["entry_id"] = existing.entry_id

    with patch.object(
        PantristOAuth2FlowHandler, "_test_credentials",
        new=AsyncMock(return_value=None),
    ):
        result = await flow.async_oauth_create_entry(
            {"token": {"access_token": "new", "list_id": LIST_ID}}
        )
    assert result["type"] == FlowResultType.ABORT
    assert result["reason"] == "reauth_successful"


async def test_reauth_step_shows_form(hass: HomeAssistant) -> None:
    """async_step_reauth_confirm with no input renders the confirm form."""
    flow = _make_flow(hass, source=SOURCE_REAUTH)
    result = await flow.async_step_reauth_confirm()
    assert result["type"] == FlowResultType.FORM
    assert result["step_id"] == "reauth_confirm"


async def test_reauth_with_input_jumps_to_user_step(hass: HomeAssistant) -> None:
    """Confirming the reauth dialog kicks off the normal OAuth flow."""
    flow = _make_flow(hass, source=SOURCE_REAUTH)
    with patch.object(
        PantristOAuth2FlowHandler, "async_step_user",
        new=AsyncMock(return_value={"type": FlowResultType.FORM, "step_id": "user"}),
    ):
        result = await flow.async_step_reauth_confirm(user_input={})
    assert result["step_id"] == "user"


async def test_reauth_dispatches_to_confirm(hass: HomeAssistant) -> None:
    """async_step_reauth always routes through reauth_confirm."""
    flow = _make_flow(hass, source=SOURCE_REAUTH)
    result = await flow.async_step_reauth({})
    assert result["type"] == FlowResultType.FORM
    assert result["step_id"] == "reauth_confirm"


async def test_fetch_list_name_uses_name_field(hass: HomeAssistant) -> None:
    """_fetch_list_name returns the `name` directly if present."""
    flow = _make_flow(hass)

    payload = [
        {"id": "other", "name": "Other"},
        {"id": LIST_ID, "name": LIST_NAME},
    ]

    class _Response:
        status = 200

        async def __aenter__(self):
            return self

        async def __aexit__(self, *exc):
            return False

        async def json(self):
            return payload

    class _Session:
        def get(self, *_args, **_kwargs):
            return _Response()

    with patch(
        "custom_components.pantrist.config_flow.aiohttp_client.async_get_clientsession",
        return_value=_Session(),
    ):
        name = await flow._fetch_list_name("token", LIST_ID)
    assert name == LIST_NAME


async def test_fetch_list_name_falls_back_to_settings(hass: HomeAssistant) -> None:
    """If `name` is missing, _fetch_list_name reads settings.name."""
    flow = _make_flow(hass)
    payload = [{"uuid": LIST_ID, "settings": {"name": "From Settings"}}]

    class _Response:
        status = 200

        async def __aenter__(self):
            return self

        async def __aexit__(self, *exc):
            return False

        async def json(self):
            return payload

    class _Session:
        def get(self, *_args, **_kwargs):
            return _Response()

    with patch(
        "custom_components.pantrist.config_flow.aiohttp_client.async_get_clientsession",
        return_value=_Session(),
    ):
        name = await flow._fetch_list_name("token", LIST_ID)
    assert name == "From Settings"


async def test_fetch_list_name_handles_http_error(hass: HomeAssistant) -> None:
    """A 500 from /list returns None instead of aborting the OAuth flow."""
    flow = _make_flow(hass)

    class _Response:
        status = 500

        async def __aenter__(self):
            return self

        async def __aexit__(self, *exc):
            return False

        async def json(self):  # pragma: no cover — not reached
            return None

    class _Session:
        def get(self, *_args, **_kwargs):
            return _Response()

    with patch(
        "custom_components.pantrist.config_flow.aiohttp_client.async_get_clientsession",
        return_value=_Session(),
    ):
        name = await flow._fetch_list_name("token", LIST_ID)
    assert name is None


async def test_fetch_list_name_handles_network_error(hass: HomeAssistant) -> None:
    """A request error returns None and logs the exception."""
    flow = _make_flow(hass)

    class _Session:
        def get(self, *_args, **_kwargs):
            raise ClientError("boom")

    with patch(
        "custom_components.pantrist.config_flow.aiohttp_client.async_get_clientsession",
        return_value=_Session(),
    ):
        name = await flow._fetch_list_name("token", LIST_ID)
    assert name is None


async def test_fetch_list_name_returns_none_for_unknown_list(
    hass: HomeAssistant,
) -> None:
    """When the requested list isn't in the response, return None."""
    flow = _make_flow(hass)
    payload = [{"id": "other", "name": "Other"}]

    class _Response:
        status = 200

        async def __aenter__(self):
            return self

        async def __aexit__(self, *exc):
            return False

        async def json(self):
            return payload

    class _Session:
        def get(self, *_args, **_kwargs):
            return _Response()

    with patch(
        "custom_components.pantrist.config_flow.aiohttp_client.async_get_clientsession",
        return_value=_Session(),
    ):
        name = await flow._fetch_list_name("token", LIST_ID)
    assert name is None


async def test_fetch_list_name_returns_none_when_payload_not_list(
    hass: HomeAssistant,
) -> None:
    """A non-list payload (e.g. error object) doesn't crash."""
    flow = _make_flow(hass)

    class _Response:
        status = 200

        async def __aenter__(self):
            return self

        async def __aexit__(self, *exc):
            return False

        async def json(self):
            return {"error": "wat"}

    class _Session:
        def get(self, *_args, **_kwargs):
            return _Response()

    with patch(
        "custom_components.pantrist.config_flow.aiohttp_client.async_get_clientsession",
        return_value=_Session(),
    ):
        name = await flow._fetch_list_name("token", LIST_ID)
    assert name is None


async def test_fetch_list_name_returns_none_without_token(hass: HomeAssistant) -> None:
    """No access token → no lookup."""
    flow = _make_flow(hass)
    assert await flow._fetch_list_name("", LIST_ID) is None


async def test_test_credentials_returns_none_on_success(hass: HomeAssistant) -> None:
    """An authenticated /list call succeeds → no error."""
    flow = _make_flow(hass)

    class _Response:
        status = 200

        async def __aenter__(self):
            return self

        async def __aexit__(self, *exc):
            return False

    class _Session:
        def get(self, *_args, **_kwargs):
            return _Response()

    with patch(
        "custom_components.pantrist.config_flow.aiohttp_client.async_get_clientsession",
        return_value=_Session(),
    ):
        result = await flow._test_credentials("token")
    assert result is None


async def test_test_credentials_returns_invalid_auth_on_401(
    hass: HomeAssistant,
) -> None:
    """A 401 surfaces as `invalid_auth`."""
    flow = _make_flow(hass)

    class _Response:
        status = 401

        async def __aenter__(self):
            return self

        async def __aexit__(self, *exc):
            return False

    class _Session:
        def get(self, *_args, **_kwargs):
            return _Response()

    with patch(
        "custom_components.pantrist.config_flow.aiohttp_client.async_get_clientsession",
        return_value=_Session(),
    ):
        result = await flow._test_credentials("token")
    assert result == "invalid_auth"


async def test_test_credentials_returns_cannot_connect_on_network_error(
    hass: HomeAssistant,
) -> None:
    """A network error surfaces as `cannot_connect`."""
    flow = _make_flow(hass)

    class _Session:
        def get(self, *_args, **_kwargs):
            raise ClientError("boom")

    with patch(
        "custom_components.pantrist.config_flow.aiohttp_client.async_get_clientsession",
        return_value=_Session(),
    ):
        result = await flow._test_credentials("token")
    assert result == "cannot_connect"


def test_extra_authorize_data_is_empty(hass: HomeAssistant) -> None:
    """No extra OAuth params — Pantrist accepts what HA already sends."""
    flow = _make_flow(hass)
    assert flow.extra_authorize_data == {}


def test_logger_is_module_logger(hass: HomeAssistant) -> None:
    """The handler exposes its module logger for HA's flow plumbing."""
    flow = _make_flow(hass)
    assert flow.logger.name == "custom_components.pantrist.config_flow"
