import logging

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback

from homeassistant.const import CONF_PASSWORD, CONF_EMAIL
from .const import DOMAIN

DATA_SCHEMA=vol.Schema({vol.Required(CONF_EMAIL): str, vol.Required(CONF_PASSWORD): str})

_LOGGER = logging.getLogger(__name__)

class GoodHomeHeaterConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Good Home Heater."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            # Attempt to connect to the API with the provided credentials
            try:
                return self.async_create_entry(title="Good Home Heater",data=user_input)
            except Exception as err:
                _LOGGER.exception("Unexpected exception", err)
                errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return GoodHomeHeaterOptionsFlowHandler(config_entry)

class GoodHomeHeaterOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle Good Home Heater options."""

    def __init__(self, config_entry):
        """Initialize Good Home Heater options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        return await self.async_step_user()

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        errors = {}
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                # Define your option schema here
            }),
            errors=errors,
        )
