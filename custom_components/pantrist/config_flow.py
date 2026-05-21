"""Config flow for the Pantrist integration."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import Any

from homeassistant.config_entries import SOURCE_REAUTH, ConfigFlowResult
from homeassistant.helpers import aiohttp_client, config_entry_oauth2_flow

from .const import API_BASE, CONF_LIST_ID, DOMAIN

_LOGGER = logging.getLogger(__name__)


class PantristOAuth2FlowHandler(
    config_entry_oauth2_flow.AbstractOAuth2FlowHandler, domain=DOMAIN
):
    """OAuth2 + list-id config flow for Pantrist."""

    DOMAIN = DOMAIN
    VERSION = 1

    @property
    def logger(self) -> logging.Logger:
        return _LOGGER

    @property
    def extra_authorize_data(self) -> dict[str, Any]:
        """Extra query params Pantrist's authorize endpoint expects."""
        return {
            # Pantrist's /access-token/authorize endpoint requires response_type=code
            # (already added by HA), state, code_challenge, code_challenge_method
            # (all handled by LocalOAuth2ImplementationWithPkce).
            # Nothing extra to add — the consent page picks the list.
        }

    async def async_step_reauth(
        self, entry_data: Mapping[str, Any]
    ) -> ConfigFlowResult:
        """Trigger reauth after a refresh-token revocation."""
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Confirm the reauth dialog with the user."""
        if user_input is None:
            return self.async_show_form(step_id="reauth_confirm")
        return await self.async_step_user()

    async def async_oauth_create_entry(
        self, data: dict[str, Any]
    ) -> ConfigFlowResult:
        """Persist the OAuth tokens + list_id returned by Pantrist."""
        token = data.get("token") or {}
        list_id = token.get("list_id")
        if not list_id:
            _LOGGER.error("Pantrist token response missing list_id")
            return self.async_abort(reason="missing_list_id")

        # Use list_id as the unique_id so the same list isn't connected twice.
        await self.async_set_unique_id(list_id)

        if self.source == SOURCE_REAUTH:
            self._abort_if_unique_id_mismatch(reason="wrong_account")
            return self.async_update_reload_and_abort(
                self._get_reauth_entry(),
                data={**data, CONF_LIST_ID: list_id},
            )

        self._abort_if_unique_id_configured()

        list_name = await self._fetch_list_name(
            token.get("access_token", ""), list_id
        )
        title = list_name or f"Pantrist (list {list_id[:8]}…)"

        return self.async_create_entry(
            title=title,
            data={**data, CONF_LIST_ID: list_id},
        )

    async def _fetch_list_name(
        self, access_token: str, list_id: str
    ) -> str | None:
        """Look up the human-readable name for the chosen list.

        The Pantrist API's `/access-token/token` response only carries the
        list UUID — the friendly name comes from `GET /list`. We fetch it
        once here to use as the config entry title.

        Best-effort: a network failure falls back to the UUID-truncated
        default title rather than aborting the flow.
        """
        if not access_token:
            return None
        try:
            session = aiohttp_client.async_get_clientsession(self.hass)
            async with session.get(
                f"{API_BASE}/list",
                headers={"Authorization": f"Bearer {access_token}"},
                timeout=10,
            ) as resp:
                if resp.status != 200:
                    return None
                lists = await resp.json()
        except Exception:  # noqa: BLE001
            _LOGGER.exception("Could not fetch list name for entry title")
            return None
        if not isinstance(lists, list):
            return None
        for entry in lists:
            if not isinstance(entry, dict):
                continue
            entry_id = entry.get("id") or entry.get("uuid")
            if entry_id != list_id:
                continue
            name = entry.get("name")
            if not name:
                settings = entry.get("settings") or {}
                if isinstance(settings, dict):
                    name = settings.get("name")
            if name:
                return str(name)
        return None
