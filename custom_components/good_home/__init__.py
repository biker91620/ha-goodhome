import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .coordinator import GoodHomeCoordinator

PLATFORMS = ["sensor", "climate", "binary_sensor"]

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config_entry: dict):
    """Set up the Good Home Heater component."""
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry):
    """Set up Good Home Heater from a config entry."""
    hass.data[DOMAIN][config_entry.entry_id] = GoodHomeCoordinator(hass, config_entry.data)

    await hass.data[DOMAIN][config_entry.entry_id].async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(config_entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    await hass.config_entries.async_forward_entry_unload(entry, "climate")
    await hass.config_entries.async_forward_entry_unload(entry, "sensor")

    # Clean up your client here if needed
    hass.data[DOMAIN].pop(entry.entry_id)

    return True
