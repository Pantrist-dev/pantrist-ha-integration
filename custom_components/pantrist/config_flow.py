"""Config flow for the Pantrist integration."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import Any

from homeassistant.config_entries import SOURCE_REAUTH, ConfigFlowResult
from homeassistant.helpers import config_entry_oauth2_flow

from .const import CONF_LIST_ID, DOMAIN

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

        return self.async_create_entry(
            title=f"Pantrist (list {list_id[:8]}…)",
            data={**data, CONF_LIST_ID: list_id},
        )
