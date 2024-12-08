import logging

from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorDeviceClass
from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

async def async_setup_entry(hass: HomeAssistant, config_entry, async_add_devices):
    """Set up entry."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    entities = []
    _LOGGER.debug(coordinator.data)
    for idx, device in enumerate(coordinator.data):
        entities.append(GoodHomeMotionSensor(coordinator, idx))
        entities.append(GoodHomeWindowSensor(coordinator, idx))

    async_add_devices(entities)


class GoodHomeMotionSensor(CoordinatorEntity, BinarySensorEntity):
    _attr_device_class = BinarySensorDeviceClass.MOTION

    def __init__(self, coordinator, idx):
        super().__init__(coordinator, context=idx)
        self.idx = idx

    @property
    def unique_id(self) -> str | None:
        return "motion_" +self.coordinator.data[self.idx].id

    @property
    def name(self):
        return self.coordinator.data[self.idx].name

    @property
    def is_on(self) -> bool | None:
        return self.coordinator.data[self.idx].state["occupancyStatus"]


class GoodHomeWindowSensor(CoordinatorEntity, BinarySensorEntity):
    _attr_device_class = BinarySensorDeviceClass.WINDOW

    def __init__(self, coordinator, idx):
        super().__init__(coordinator, context=idx)
        self.idx = idx

    @property
    def unique_id(self) -> str | None:
        return "window_" +self.coordinator.data[self.idx].id

    @property
    def name(self):
        return self.coordinator.data[self.idx].name

    @property
    def is_on(self) -> bool | None:
        return self.coordinator.data[self.idx].state["window"]