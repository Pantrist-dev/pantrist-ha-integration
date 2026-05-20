import time

import httpx
import pytest
import respx

from credentials import Credentials
from oauth_flow import OAuthError, OAuthFlow

REDIRECT_URI = "http://homeassistant.local:8123/api/hassio_ingress/abc/oauth/callback"
APP_BASE = "https://app.pantrist.app"
API_BASE = "https://api.pantrist.app"


def test_begin_returns_authorize_url_with_pkce():
    flow = OAuthFlow(app_base=APP_BASE, api_base=API_BASE)
    url = flow.begin(REDIRECT_URI)
    assert url.startswith(f"{APP_BASE}/oauth/authorize?")
    assert "client_id=pantrist-ha-addon" in url
    assert "code_challenge_method=S256" in url
    assert "code_challenge=" in url
    assert "state=" in url
    assert "redirect_uri=" in url


def test_complete_rejects_state_mismatch():
    flow = OAuthFlow(app_base=APP_BASE, api_base=API_BASE)
    flow.begin(REDIRECT_URI)
    with pytest.raises(OAuthError, match="state_mismatch"):
        flow.complete(code="code-1", state="not-the-state", redirect_uri=REDIRECT_URI)


def test_complete_rejects_when_begin_not_called():
    flow = OAuthFlow(app_base=APP_BASE, api_base=API_BASE)
    with pytest.raises(OAuthError, match="no_pending"):
        flow.complete(code="c", state="s", redirect_uri=REDIRECT_URI)


def test_complete_rejects_expired_pending():
    flow = OAuthFlow(app_base=APP_BASE, api_base=API_BASE)
    flow.begin(REDIRECT_URI)
    # Force the pending timestamp 11 minutes in the past
    pending = flow._pending  # type: ignore[attr-defined]
    flow._pending = pending._replace(created_at=time.time() - 660)  # type: ignore[attr-defined]
    with pytest.raises(OAuthError, match="expired"):
        flow.complete(code="c", state=flow._pending.state, redirect_uri=REDIRECT_URI)  # type: ignore[attr-defined]


@respx.mock
def test_complete_exchanges_code_for_credentials():
    flow = OAuthFlow(app_base=APP_BASE, api_base=API_BASE)
    flow.begin(REDIRECT_URI)
    state = flow._pending.state  # type: ignore[attr-defined]

    respx.post(f"{API_BASE}/access-token/token").mock(
        return_value=httpx.Response(
            200,
            json={
                "access_token": "at-1",
                "refresh_token": "rt-1",
                "token_type": "Bearer",
                "expires_in": 3600,
                "list_id": "list-1",
            },
        )
    )

    creds = flow.complete(code="code-1", state=state, redirect_uri=REDIRECT_URI)
    assert creds == Credentials(refresh_token="rt-1", list_id="list-1")


@respx.mock
def test_complete_raises_on_api_error():
    flow = OAuthFlow(app_base=APP_BASE, api_base=API_BASE)
    flow.begin(REDIRECT_URI)
    state = flow._pending.state  # type: ignore[attr-defined]

    respx.post(f"{API_BASE}/access-token/token").mock(
        return_value=httpx.Response(401, json={"error": "invalid_grant"})
    )

    with pytest.raises(OAuthError, match="invalid_grant"):
        flow.complete(code="code-1", state=state, redirect_uri=REDIRECT_URI)


@respx.mock
def test_complete_includes_redirect_uri_and_code_verifier_in_payload():
    flow = OAuthFlow(app_base=APP_BASE, api_base=API_BASE)
    flow.begin(REDIRECT_URI)
    state = flow._pending.state  # type: ignore[attr-defined]
    expected_verifier = flow._pending.code_verifier  # type: ignore[attr-defined]

    route = respx.post(f"{API_BASE}/access-token/token").mock(
        return_value=httpx.Response(
            200,
            json={
                "access_token": "at-1",
                "refresh_token": "rt-1",
                "token_type": "Bearer",
                "expires_in": 3600,
                "list_id": "list-1",
            },
        )
    )

    flow.complete(code="code-1", state=state, redirect_uri=REDIRECT_URI)
    request = route.calls.last.request
    import json as _json
    payload = _json.loads(request.content)
    assert payload["grant_type"] == "authorization_code"
    assert payload["code"] == "code-1"
    assert payload["code_verifier"] == expected_verifier
    assert payload["client_id"] == "pantrist-ha-addon"
    assert payload["redirect_uri"] == REDIRECT_URI
