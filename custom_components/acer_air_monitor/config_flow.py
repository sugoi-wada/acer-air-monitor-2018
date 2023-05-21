"""Adds config flow for Acer air monitor."""
from __future__ import annotations

# import logging

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_PASSWORD, CONF_EMAIL
from homeassistant.helpers import selector
from homeassistant.helpers.aiohttp_client import async_create_clientsession

from .lib.api import (
    AirMonitorAuthApiClient,
    ClientAuthenticationError,
    ClientCommunicationError,
    ClientError,
)
from .const import DOMAIN, LOGGER, USER_ATTR


class ConfigFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Acer Air Monitor."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict | None = None
    ) -> config_entries.FlowResult:
        """Handle a flow initialized by the user."""
        _errors = {}

        if user_input is not None:
            try:
                ret = await self._try_login(
                    user_input[CONF_EMAIL], user_input[CONF_PASSWORD]
                )

                await self.async_set_unique_id(ret["data"]["id"])
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=user_input[CONF_EMAIL],
                    data=user_input | {USER_ATTR: ret["data"]},
                )
            except ClientAuthenticationError as exception:
                LOGGER.warning(exception)
                _errors["base"] = "auth"
            except ClientCommunicationError as exception:
                LOGGER.error(exception)
                _errors["base"] = "connection"
            except ClientError as exception:
                LOGGER.exception(exception)
                _errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_EMAIL,
                        default=(user_input or {}).get(CONF_EMAIL),
                    ): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.EMAIL
                        ),
                    ),
                    vol.Required(CONF_PASSWORD): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.PASSWORD
                        ),
                    ),
                }
            ),
            errors=_errors,
        )

    async def _try_login(self, email: str, password: str) -> dict:
        """Return response if login succeeded."""
        client = AirMonitorAuthApiClient(
            email=email,
            password=password,
            session=async_create_clientsession(self.hass),
        )
        return await client.login()
