import logging

from homeassistant.components.climate import ClimateEntity
from homeassistant.components.climate.const import (
    SUPPORT_TARGET_TEMPERATURE, HVACMode)
from homeassistant.const import UnitOfTemperature
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

SUPPORT_FLAGS = SUPPORT_TARGET_TEMPERATURE

async def async_setup_entry(hass, config_entry, async_add_devices):
    """Set up entry."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    async_add_devices([GoodHomeHeater(coordinator, idx) for idx, device in enumerate(coordinator.data)])


class GoodHomeHeater(ClimateEntity, CoordinatorEntity):

    def __init__(self, coordinator, idx):
        super().__init__(coordinator, context=idx)
        self.idx = idx

    @property
    def name(self):
        return self.coordinator.data[self.idx].name

    @property
    def unique_id(self):
        return self.coordinator.data[self.idx].id

#    @property
#    def supported_features(self):
#        return [ClimateEntityFeature.TURN_OFF, ClimateEntityFeature.TURN_ON, ClimateEntityFeature.TARGET_TEMPERATURE]

    @property
    def hvac_mode(self):
        return HVACMode.AUTO

    @property
    def hvac_modes(self):
        return [HVACMode.OFF, HVACMode.AUTO, HVACMode.HEAT]

    @property
    def temperature_unit(self) -> str:
        return UnitOfTemperature.CELSIUS

    @property
    def current_temperature(self) -> float | None :
        return self.coordinator.data[self.idx].state["currentTemp"]

    @property
    def current_humidity(self) -> float | None:
        return self.coordinator.data[self.idx].state["humidity"]

