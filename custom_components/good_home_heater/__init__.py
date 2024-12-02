import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Good Home Heater component."""
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Good Home Heater from a config entry."""
    username = entry.data["username"]
    password = entry.data["password"]

    # Initialize your API client with credentials
    hass.data[DOMAIN][entry.entry_id] = GoodHomeClient(username, password)

    # Forward the setup to the platforms (climate, sensor)
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "climate")
    )
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    await hass.config_entries.async_forward_entry_unload(entry, "climate")
    await hass.config_entries.async_forward_entry_unload(entry, "sensor")

    # Clean up your client here if needed
    hass.data[DOMAIN].pop(entry.entry_id)

    return True
