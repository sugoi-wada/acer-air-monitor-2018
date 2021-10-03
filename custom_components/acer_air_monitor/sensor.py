"""Sensor platform for acer_air_monitor."""
from typing import Union

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import StateType

from custom_components.acer_air_monitor import AirMonitorDataUpdateCoordinator
from custom_components.acer_air_monitor.lib.sensor_type import SensorType

from .const import DOMAIN
from .entity import AirMonitorEntity


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities
) -> None:
    """Setup sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        [
            AirMonitorSensor(coordinator, index, sensor_key)
            for index, device in enumerate(coordinator.data)
            for sensor_key in device["sensors"]
            if AIR_MONITOR_SENSOR.get(sensor_key) is not None
        ]
    )


AIR_MONITOR_SENSOR: dict[SensorType, tuple[str, Union[str, None], str, str]] = {
    # NOTE: tuple(name, device_class, unit, icon)
    SensorType.CO2: ("CO2", "carbon_dioxide", "ppm", "mdi:molecule-co2"),
    SensorType.PM25: ("PM25", "pm25", "µg/m³", "mdi:chart-scatter-plot"),
    SensorType.PM10: ("PM10", "pm100", "µg/m³", "mdi:chart-scatter-plot-hexbin"),
    SensorType.ILLUMINANCE: ("Illuminance", "illuminance", "lx", "mdi:weather-sunny"),
    SensorType.HUMIDITY: ("Humidity", "humidity", "%", "mdi:water-percent"),
    SensorType.TEMPERATURE: ("Temperature", "temperature", "°C", "mdi:thermometer"),
    SensorType.TVOC: ("TVOC", None, "ppb", "mdi:air-filter"),
    SensorType.IAQ: ("IAQ", None, "IAQ", "mdi:weather-windy"),
}


class AirMonitorSensor(AirMonitorEntity):
    """Air Monitor Sensor class."""

    def __init__(
        self,
        coordinator: AirMonitorDataUpdateCoordinator,
        device_index: int,
        sensor_key: str,
    ):
        super().__init__(coordinator, device_index)
        self._sensor_key = sensor_key

    @property
    def unique_id(self) -> Union[str, None]:
        """Return a unique ID to use for this entity."""
        return f"{self.device['device_id']}_{self._sensor_key}"

    @property
    def name(self) -> Union[str, None]:
        """Return the name of the sensor."""
        return f"{self.device['name']} {AIR_MONITOR_SENSOR[self._sensor_key][0]}"

    @property
    def state(self) -> StateType:
        """Return the state of the sensor."""
        return self.coordinator.data[self.device_index]["sensors"][self._sensor_key]

    @property
    def device_class(self) -> Union[str, None]:
        """Return the device class of the sensor."""
        return AIR_MONITOR_SENSOR[self._sensor_key][1]

    @property
    def unit_of_measurement(self) -> Union[str, None]:
        """Return the unit of measurement of the sensor."""
        return AIR_MONITOR_SENSOR[self._sensor_key][2]

    @property
    def icon(self) -> Union[str, None]:
        """Return the icon of the sensor."""
        return AIR_MONITOR_SENSOR[self._sensor_key][3]
