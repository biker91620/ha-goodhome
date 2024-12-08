import logging

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass, SensorStateClass
from homeassistant.const import UnitOfTemperature

_LOGGER = logging.getLogger(__name__)
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

async def async_setup_entry(hass, config_entry, async_add_devices):
    """Set up entry."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    entities = []
    _LOGGER.debug(coordinator.data)
    for idx, device in enumerate(coordinator.data):
        entities.append(GoodHomeTemperatureSensor(coordinator, idx))
        entities.append(GoodHomeHumiditySensor(coordinator, idx))
    async_add_devices(entities)


class GoodHomeTemperatureSensor(CoordinatorEntity, SensorEntity):
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, coordinator, idx):
        super().__init__(coordinator, context=idx)
        self.idx = idx

    @property
    def unique_id(self) -> str | None:
        return "temperature_" +self.coordinator.data[self.idx].id

    @property
    def name(self):
        return self.coordinator.data[self.idx].name

    @property
    def native_temperature(self) -> float:
        return self.coordinator.data[self.idx].state["currentTemp"]


class GoodHomeHumiditySensor(CoordinatorEntity, SensorEntity):
    _attr_device_class = SensorDeviceClass.HUMIDITY
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, coordinator, idx):
        super().__init__(coordinator, context=idx)
        self.idx = idx

    @property
    def unique_id(self) -> str | None:
        return "humidity_" +self.coordinator.data[self.idx].id

    @property
    def name(self):
        return self.coordinator.data[self.idx].name

    @property
    def native_temperature(self) -> float:
        return self.coordinator.data[self.idx].state["humidity"]
