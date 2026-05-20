from unittest.mock import MagicMock

import pytest
from aiohttp.test_utils import TestClient, TestServer

from credentials import Credentials


@pytest.fixture
def state():
    s = MagicMock()
    s.get_credentials = MagicMock(return_value=None)
    s.session = MagicMock(is_running=False)
    s.oauth_flow = MagicMock()
    s.custom_ha_url = ""
    s.get_list_name = MagicMock(return_value=None)
    return s


@pytest.mark.asyncio
async def test_status_page_disconnected(state):
    from ingress_server import make_ingress_app
    app = make_ingress_app(state)
    async with TestClient(TestServer(app)) as client:
        resp = await client.get("/", headers={"X-Ingress-Path": "/api/hassio_ingress/abc"})
        assert resp.status == 200
        text = await resp.text()
        assert "Connect" in text


@pytest.mark.asyncio
async def test_status_page_connected(state):
    from ingress_server import make_ingress_app
    state.get_credentials.return_value = Credentials(refresh_token="rt", list_id="list-1")
    state.session.is_running = True
    state.get_list_name.return_value = "Home"
    app = make_ingress_app(state)
    async with TestClient(TestServer(app)) as client:
        resp = await client.get("/", headers={"X-Ingress-Path": "/api/hassio_ingress/abc"})
        assert resp.status == 200
        text = await resp.text()
        assert "Connected" in text
        assert "Home" in text


@pytest.mark.asyncio
async def test_oauth_start_redirects_to_pantrist(state):
    from ingress_server import make_ingress_app
    state.oauth_flow.begin.return_value = "https://app.pantrist.app/oauth/authorize?stub"
    app = make_ingress_app(state)
    async with TestClient(TestServer(app)) as client:
        resp = await client.get(
            "/oauth/start",
            headers={
                "X-Ingress-Path": "/api/hassio_ingress/abc",
                "X-Forwarded-Proto": "http",
                "Host": "homeassistant.local:8123",
            },
            allow_redirects=False,
        )
        assert resp.status == 302
        assert resp.headers["Location"].startswith("https://app.pantrist.app/oauth/authorize")
        state.oauth_flow.begin.assert_called_once()
        called_redirect = state.oauth_flow.begin.call_args.args[0]
        # Verify redirect_uri assembled from X-Ingress-Path + X-Forwarded-Proto + Host
        assert called_redirect == "http://homeassistant.local:8123/api/hassio_ingress/abc/oauth/callback"


@pytest.mark.asyncio
async def test_oauth_start_uses_custom_ha_url_when_set(state):
    from ingress_server import make_ingress_app
    state.custom_ha_url = "https://ha.example.com/"  # trailing slash should be stripped
    state.oauth_flow.begin.return_value = "https://app.pantrist.app/oauth/authorize?stub"
    app = make_ingress_app(state)
    async with TestClient(TestServer(app)) as client:
        await client.get(
            "/oauth/start",
            headers={"X-Ingress-Path": "/api/hassio_ingress/abc"},
            allow_redirects=False,
        )
        called_redirect = state.oauth_flow.begin.call_args.args[0]
        assert called_redirect == "https://ha.example.com/api/hassio_ingress/abc/oauth/callback"


@pytest.mark.asyncio
async def test_oauth_callback_completes_and_starts_session(state):
    from ingress_server import make_ingress_app
    state.oauth_flow.complete.return_value = Credentials(refresh_token="rt", list_id="list-1")
    state.save_credentials = MagicMock()
    state.start_session = MagicMock()
    app = make_ingress_app(state)
    async with TestClient(TestServer(app)) as client:
        resp = await client.get(
            "/oauth/callback?code=c&state=s",
            headers={
                "X-Ingress-Path": "/api/hassio_ingress/abc",
                "X-Forwarded-Proto": "http",
                "Host": "homeassistant.local:8123",
            },
            allow_redirects=False,
        )
        assert resp.status == 302
        state.oauth_flow.complete.assert_called_once()
        state.save_credentials.assert_called_once_with(Credentials(refresh_token="rt", list_id="list-1"))
        state.start_session.assert_called_once()


@pytest.mark.asyncio
async def test_oauth_callback_with_error_does_not_save(state):
    from ingress_server import make_ingress_app
    state.save_credentials = MagicMock()
    state.start_session = MagicMock()
    app = make_ingress_app(state)
    async with TestClient(TestServer(app)) as client:
        resp = await client.get(
            "/oauth/callback?error=access_denied&state=s",
            headers={"X-Ingress-Path": "/api/hassio_ingress/abc"},
            allow_redirects=False,
        )
        # Should be a redirect (302) with the error visible somewhere
        assert resp.status == 302
        state.oauth_flow.complete.assert_not_called()
        state.save_credentials.assert_not_called()


@pytest.mark.asyncio
async def test_oauth_callback_missing_code_returns_400(state):
    from ingress_server import make_ingress_app
    app = make_ingress_app(state)
    async with TestClient(TestServer(app)) as client:
        resp = await client.get(
            "/oauth/callback",
            headers={"X-Ingress-Path": "/api/hassio_ingress/abc"},
            allow_redirects=False,
        )
        assert resp.status == 400


@pytest.mark.asyncio
async def test_disconnect_clears_creds_and_stops_session(state):
    from ingress_server import make_ingress_app
    state.clear_credentials = MagicMock()
    state.stop_session = MagicMock()
    state.ha_client = MagicMock()
    app = make_ingress_app(state)
    async with TestClient(TestServer(app)) as client:
        resp = await client.post(
            "/disconnect", headers={"X-Ingress-Path": "/api/hassio_ingress/abc"}, allow_redirects=False
        )
        assert resp.status == 302
        state.clear_credentials.assert_called_once()
        state.stop_session.assert_called_once()
