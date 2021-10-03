"""Adds config flow for Acer air monitor."""
import logging

from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_create_clientsession
import voluptuous as vol

from .const import CONF_EMAIL, CONF_PASSWORD, DOMAIN, USER_ATTR
from .lib.api import AirMonitorAuthApiClient

_LOGGER: logging.Logger = logging.getLogger(__package__)


class ConfigFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow handler."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize."""
        self._errors = {}

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        self._errors = {}

        # Uncomment the next 2 lines if only a single instance of the integration is allowed:
        # if self._async_current_entries():
        #     return self.async_abort(reason="single_instance_allowed")

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
            except Exception as exception:  # pylint: disable=broad-except
                _LOGGER.error(exception)
                self._errors["base"] = "auth"

            return await self._show_config_form(user_input)

        user_input = {}
        # Provide defaults for form
        user_input[CONF_EMAIL] = ""
        user_input[CONF_PASSWORD] = ""

        return await self._show_config_form(user_input)

    async def _show_config_form(
        self, user_input: dict
    ):  # pylint: disable=unused-argument
        """Show the configuration form to edit location data."""
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_EMAIL, default=user_input[CONF_EMAIL]): str,
                    vol.Required(CONF_PASSWORD, default=user_input[CONF_PASSWORD]): str,
                }
            ),
            errors=self._errors,
        )

    async def _try_login(self, email: str, password: str) -> dict:
        """Return response if login succeeded."""
        session = async_create_clientsession(self.hass)
        client = AirMonitorAuthApiClient(email, password, session)
        return await client.login()
