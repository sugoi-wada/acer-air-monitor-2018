"""BlueprintEntity class"""
from typing import Union

from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from custom_components.acer_air_monitor import AirMonitorDataUpdateCoordinator

from .const import DOMAIN, MANUFACTURER


class AirMonitorEntity(CoordinatorEntity):
    def __init__(self, coordinator: AirMonitorDataUpdateCoordinator, device_index: int):
        super().__init__(coordinator)
        self.device_index = device_index

    @property
    def device(self) -> dict:
        """Return a device dict"""
        return self.coordinator.data[self.device_index]

    @property
    def device_info(self) -> Union[DeviceInfo, None]:
        return {
            "identifiers": {(DOMAIN, self.device["device_id"])},
            "name": self.device["name"],
            "model": self.device["modelName"],
            "manufacturer": MANUFACTURER,
            "mac": self.device["mac"],
        }
