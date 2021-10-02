"""Adds config flow for Acer air monitor."""
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.aiohttp_client import async_create_clientsession
import voluptuous as vol
import logging
from .lib.api import AirMonitorAuthApiClient
from .const import CONF_PASSWORD, CONF_EMAIL, DOMAIN, PLATFORMS, USER_ATTR

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

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return OptionsFlowHandler(config_entry)

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


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Config flow options handler."""

    def __init__(self, config_entry):
        """Initialize HACS options flow."""
        self.config_entry = config_entry
        self.options = dict(config_entry.options)

    async def async_step_init(self, user_input=None):  # pylint: disable=unused-argument
        """Manage the options."""
        return await self.async_step_user()

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        if user_input is not None:
            self.options.update(user_input)
            return await self._update_options()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(x, default=self.options.get(x, True)): bool
                    for x in sorted(PLATFORMS)
                }
            ),
        )

    async def _update_options(self):
        """Update config entry options."""
        return self.async_create_entry(
            title=self.config_entry.data.get(CONF_EMAIL), data=self.options
        )