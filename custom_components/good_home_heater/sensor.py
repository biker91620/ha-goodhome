import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import TEMP_CELSIUS, HUMIDITY_PERCENTAGE
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up Good Home Heater sensors based on a config entry."""
    client = hass.data[DOMAIN][config_entry.entry_id]

    # Fetch initial data (if necessary)
    devices = await hass.async_add_executor_job(client.get_devices)

    sensors = []
    for device in devices:
        sensors.append(GoodHomeTemperatureSensor(device))
        sensors.append(GoodHomeHumiditySensor(device))

    async_add_entities(sensors)

class GoodHomeTemperatureSensor(SensorEntity):
    def __init__(self, device):
        self._device = device
        self._name = f"{device.name} Temperature"
        self._state = device.temperature

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def unit_of_measurement(self):
        return TEMP_CELSIUS

    @property
    def device_class(self):
        return "temperature"

    async def async_update(self):
        await self.hass.async_add_executor_job(self._device.update)
        self._state = self._device.temperature

class GoodHomeHumiditySensor(SensorEntity):
    def __init__(self, device):
        self._device = device
        self._name = f"{device.name} Humidity"
        self._state = device.humidity

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def unit_of_measurement(self):
        return HUMIDITY_PERCENTAGE

    @property
    def device_class(self):
        return "humidity"

    async def async_update(self):
        await self.hass.async_add_executor_job(self._device.update)
        self._state = self._device.humidity
