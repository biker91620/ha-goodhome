import logging

from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorDeviceClass

_LOGGER = logging.getLogger(__name__)
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

async def async_setup_entry(hass, config_entry, async_add_devices):
    """Set up entry."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    async_add_devices([GoodHomeMotionSensor(coordinator, idx) for idx, devices in enumerate(coordinator.data)])


class GoodHomeMotionSensor(CoordinatorEntity, BinarySensorEntity):
    _attr_device_class = BinarySensorDeviceClass.MOTION

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
    def is_on(self) -> bool | None:
        return self.coordinator.data[self.idx].state["occupancyStatus"]
