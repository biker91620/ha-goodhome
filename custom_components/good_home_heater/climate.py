import logging
from homeassistant.components.climate import ClimateEntity
from homeassistant.components.climate.const import (
    HVAC_MODE_OFF, HVAC_MODE_HEAT, SUPPORT_TARGET_TEMPERATURE)
from homeassistant.const import TEMP_CELSIUS, ATTR_TEMPERATURE
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

SUPPORT_FLAGS = SUPPORT_TARGET_TEMPERATURE

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up Good Home Heater based on a config entry."""
    client = hass.data[DOMAIN][config_entry.entry_id]

    # Fetch initial data (if necessary)
    devices = await hass.async_add_executor_job(client.get_devices)

    async_add_entities([GoodHomeHeater(device) for device in devices])

class GoodHomeHeater(ClimateEntity):
    def __init__(self, device):
        self._device = device

        self._name = device.name
        self._supported_features = SUPPORT_FLAGS

        self._hvac_mode = HVAC_MODE_HEAT if device.is_on else HVAC_MODE_OFF
        self._target_temperature = device.target_temperature

    @property
    def name(self):
        return self._name

    @property
    def supported_features(self):
        return self._supported_features

    @property
    def hvac_mode(self):
        return self._hvac_mode

    @property
    def hvac_modes(self):
        return [HVAC_MODE_HEAT, HVAC_MODE_OFF]

    @property
    def temperature_unit(self):
        return TEMP_CELSIUS

    @property
    def target_temperature(self):
        return self._target_temperature

    async def async_set_temperature(self, **kwargs):
        if ATTR_TEMPERATURE in kwargs:
            self._target_temperature = kwargs[ATTR_TEMPERATURE]
            await self.hass.async_add_executor_job(
                lambda: self._device.set_temperature(kwargs[ATTR_TEMPERATURE])
            )

    async def async_set_hvac_mode(self, hvac_mode):
        self._hvac_mode = hvac_mode
        if hvac_mode == HVAC_MODE_HEAT:
            await self.hass.async_add_executor_job(lambda: self._device.turn_on())
        else:
            await self.hass.async_add_executor_job(lambda: self._device.turn_off())
