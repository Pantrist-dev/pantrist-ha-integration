"""OAuth 2.0 PKCE flow for the Pantrist HA addon."""

from __future__ import annotations

import base64
import hashlib
import logging
import secrets
import time
from dataclasses import dataclass
from typing import NamedTuple
from urllib.parse import urlencode

import httpx

from credentials import Credentials

logger = logging.getLogger(__name__)

CLIENT_ID = "pantrist-ha-addon"
PENDING_TTL_SECONDS = 600  # matches API auth-code TTL


class OAuthError(Exception):
    pass


class PendingAuth(NamedTuple):
    state: str
    code_verifier: str
    created_at: float


@dataclass
class OAuthFlow:
    app_base: str = "https://app.pantrist.app"
    api_base: str = "https://api.pantrist.app"
    _pending: PendingAuth | None = None

    def begin(self, redirect_uri: str) -> str:
        code_verifier = secrets.token_urlsafe(48)
        digest = hashlib.sha256(code_verifier.encode()).digest()
        code_challenge = base64.urlsafe_b64encode(digest).rstrip(b"=").decode()
        state = secrets.token_urlsafe(24)
        self._pending = PendingAuth(
            state=state, code_verifier=code_verifier, created_at=time.time()
        )
        params = {
            "response_type": "code",
            "client_id": CLIENT_ID,
            "code_challenge": code_challenge,
            "code_challenge_method": "S256",
            "redirect_uri": redirect_uri,
            "state": state,
        }
        return f"{self.app_base}/oauth/authorize?{urlencode(params)}"

    def complete(self, code: str, state: str, redirect_uri: str) -> Credentials:
        pending = self._pending
        if not pending:
            raise OAuthError("no_pending")
        if pending.state != state:
            raise OAuthError("state_mismatch")
        if time.time() - pending.created_at > PENDING_TTL_SECONDS:
            self._pending = None
            raise OAuthError("expired")

        try:
            response = httpx.post(
                f"{self.api_base}/access-token/token",
                json={
                    "grant_type": "authorization_code",
                    "code": code,
                    "code_verifier": pending.code_verifier,
                    "client_id": CLIENT_ID,
                    "redirect_uri": redirect_uri,
                },
                timeout=15,
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            try:
                body = exc.response.json()
            except ValueError:
                body = {}
            raise OAuthError(body.get("error", f"http_{exc.response.status_code}")) from exc
        except httpx.RequestError as exc:
            raise OAuthError(f"network_error: {exc}") from exc

        data = response.json()
        if "refresh_token" not in data or "list_id" not in data:
            raise OAuthError("malformed_token_response")
        self._pending = None
        return Credentials(refresh_token=data["refresh_token"], list_id=data["list_id"])
