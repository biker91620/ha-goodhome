import logging
from datetime import timedelta

from goodhomepy import GoodHomeClient

from homeassistant.const import CONF_PASSWORD, CONF_EMAIL

from goodhomepy import AuthResponse
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

_LOGGER = logging.getLogger(__name__)

class GoodHomeCoordinator(DataUpdateCoordinator):
    auth:AuthResponse = None
    client:GoodHomeClient = None

    def __init__(self, hass, parameters):
        super().__init__(
            hass,
            _LOGGER,
            name="Good Home coordinator",
            update_interval=timedelta(seconds=30),
            update_method=self.async_update_data,
            always_update=True
        )
        self.email = parameters[CONF_EMAIL]
        self.password = parameters[CONF_PASSWORD]

    async def async_update_data(self):
        try:
            self.client = GoodHomeClient()
            self.auth = await self.client.login(self.email, self.password)
            self.client.token = self.auth.token
        except Exception as err:
            raise UpdateFailed(f"Unable to login: ${err}")
        try:
            self.logger.debug("Fetching devices")
            devices = await self.client.get_devices(self.auth.id)
            self.logger.debug(f"Found {len(devices)} devices")
            return devices
        except Exception as err:
            raise UpdateFailed(f"Unable to update data: ${err}")
