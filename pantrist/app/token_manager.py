"""OAuth access token manager for automatic refresh.

Uses the Pantrist /access-token OAuth 2.0 endpoint with a refresh_token grant.
Refresh tokens rotate on each use — the new token is persisted in memory.
"""

import logging
import threading
from typing import Callable

import httpx

logger = logging.getLogger(__name__)

_TOKEN_ENDPOINT = "https://api.pantrist.app/access-token/token"
_CLIENT_ID = "pantrist-ha-addon"
# Refresh 10 minutes before expiry to avoid using a token that's about to expire.
_REFRESH_BUFFER_SECONDS = 600


class TokenRefreshError(Exception):
    pass


class TokenManager:
    """Fetches and auto-refreshes an OAuth access token using a refresh token."""

    def __init__(
        self,
        refresh_token: str,
        on_token_updated: Callable[[str], None],
        on_failure: Callable[[], None] | None = None,
    ) -> None:
        self._refresh_token = refresh_token
        self._on_token_updated = on_token_updated
        self._on_failure = on_failure
        self._access_token: str = ""
        self._expires_in: int = 3600
        self._unauthorized_failures = 0
        self._stop = threading.Event()
        self._thread = threading.Thread(
            target=self._run, daemon=True, name="pantrist-token"
        )

    @property
    def access_token(self) -> str:
        return self._access_token

    def start(self) -> None:
        """Synchronously perform an initial refresh, then start the background loop."""
        self._do_refresh()
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()

    def _record_unauthorized(self) -> None:
        """Increment the consecutive-401 counter and fire the failure callback at 3."""
        self._unauthorized_failures += 1
        if self._unauthorized_failures >= 3 and self._on_failure is not None:
            self._unauthorized_failures = 0
            try:
                self._on_failure()
            except Exception:
                logger.exception("on_failure callback raised an exception")

    def _record_success(self) -> None:
        """Reset the consecutive-401 counter after a successful refresh."""
        self._unauthorized_failures = 0

    def _run(self) -> None:
        while not self._stop.is_set():
            sleep_seconds = max(self._expires_in - _REFRESH_BUFFER_SECONDS, 60)
            logger.debug("Next token refresh in %d s", sleep_seconds)
            self._stop.wait(timeout=sleep_seconds)
            if self._stop.is_set():
                break
            try:
                self._do_refresh()
                self._record_success()
            except TokenRefreshError as exc:
                logger.exception("Token refresh failed; retrying in 60 s")
                if "HTTP 401" in str(exc):
                    self._record_unauthorized()
                self._stop.wait(timeout=60)
            except Exception:
                logger.exception("Token refresh failed; retrying in 60 s")
                self._stop.wait(timeout=60)

    def _do_refresh(self) -> None:
        try:
            response = httpx.post(
                _TOKEN_ENDPOINT,
                json={
                    "grant_type": "refresh_token",
                    "refresh_token": self._refresh_token,
                    "client_id": _CLIENT_ID,
                },
                timeout=15,
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise TokenRefreshError(
                f"Token refresh failed: HTTP {exc.response.status_code} – {exc.response.text}"
            ) from exc
        except httpx.RequestError as exc:
            raise TokenRefreshError(f"Token refresh request error: {exc}") from exc

        data = response.json()
        self._access_token = data["access_token"]
        self._expires_in = int(data.get("expires_in", 3600))

        # Refresh tokens rotate — store the new one.
        new_refresh = data.get("refresh_token")
        if new_refresh:
            self._refresh_token = new_refresh

        logger.info("Access token refreshed (expires in %d s)", self._expires_in)
        self._on_token_updated(self._access_token)
