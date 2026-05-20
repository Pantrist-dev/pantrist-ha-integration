from unittest.mock import MagicMock

import httpx
import respx

import token_manager as tm


@respx.mock
def test_three_consecutive_401_refreshes_invoke_on_failure():
    on_failure = MagicMock()
    on_update = MagicMock()

    respx.post(tm._TOKEN_ENDPOINT).mock(
        return_value=httpx.Response(401, json={"error": "invalid_grant"})
    )

    mgr = tm.TokenManager(
        refresh_token="rt-bad",
        on_token_updated=on_update,
        on_failure=on_failure,
    )
    # Drive refresh attempts directly (no background thread)
    for _ in range(3):
        try:
            mgr._do_refresh()  # type: ignore[attr-defined]
        except tm.TokenRefreshError:
            mgr._record_unauthorized()  # type: ignore[attr-defined]
        else:
            mgr._record_success()  # type: ignore[attr-defined]

    on_failure.assert_called_once()


@respx.mock
def test_single_5xx_failure_does_not_trigger_callback():
    on_failure = MagicMock()
    respx.post(tm._TOKEN_ENDPOINT).mock(return_value=httpx.Response(503))
    mgr = tm.TokenManager(
        refresh_token="rt",
        on_token_updated=lambda t: None,
        on_failure=on_failure,
    )
    try:
        mgr._do_refresh()  # type: ignore[attr-defined]
    except tm.TokenRefreshError:
        mgr._record_unauthorized()  # type: ignore[attr-defined]
    on_failure.assert_not_called()


@respx.mock
def test_successful_refresh_resets_counter():
    on_failure = MagicMock()
    on_update = MagicMock()

    # First two return 401; third returns success
    respx.post(tm._TOKEN_ENDPOINT).mock(
        side_effect=[
            httpx.Response(401, json={"error": "invalid_grant"}),
            httpx.Response(401, json={"error": "invalid_grant"}),
            httpx.Response(200, json={"access_token": "at-1", "refresh_token": "rt-2", "expires_in": 3600}),
            httpx.Response(401, json={"error": "invalid_grant"}),
            httpx.Response(401, json={"error": "invalid_grant"}),
        ]
    )

    mgr = tm.TokenManager(
        refresh_token="rt",
        on_token_updated=on_update,
        on_failure=on_failure,
    )
    for _ in range(5):
        try:
            mgr._do_refresh()  # type: ignore[attr-defined]
        except tm.TokenRefreshError:
            mgr._record_unauthorized()  # type: ignore[attr-defined]
        else:
            mgr._record_success()  # type: ignore[attr-defined]

    # After 2 failures, then success (reset to 0), then 2 more failures (< 3)
    on_failure.assert_not_called()
