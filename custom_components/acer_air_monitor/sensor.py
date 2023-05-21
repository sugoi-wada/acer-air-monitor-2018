"""Sensor platform for acer_air_monitor."""
from __future__ import annotations


from homeassistant.components.sensor import (
    ENTITY_ID_FORMAT,
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    CONCENTRATION_PARTS_PER_BILLION,
    CONCENTRATION_PARTS_PER_MILLION,
    LIGHT_LUX,
    PERCENTAGE,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import generate_entity_id

from .const import DOMAIN
from .coordinator import AirMonitorDataUpdateCoordinator
from .entity import AirMonitorEntity
from .lib.sensor_type import SensorType


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities
) -> None:
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        [
            AirMonitorSensor(
                coordinator=coordinator,
                entity_description=AIR_MONITOR_SENSOR[sensor_key],
                sensor_key=sensor_key,
                entity_id=generate_entity_id(
                    ENTITY_ID_FORMAT, f"acer_air_monitor_{sensor_key}", hass=hass
                ),
            )
            for sensor_key in coordinator.data["sensors"]
            if AIR_MONITOR_SENSOR.get(sensor_key) is not None
        ]
    )


AIR_MONITOR_SENSOR: dict[SensorType, SensorEntityDescription] = {
    SensorType.CO2: SensorEntityDescription(
        key=SensorType.CO2,
        name="CO2",
        device_class=SensorDeviceClass.CO2,
        native_unit_of_measurement=CONCENTRATION_PARTS_PER_MILLION,
        icon="mdi:molecule-co2",
    ),
    SensorType.PM25: SensorEntityDescription(
        key=SensorType.PM25,
        name="PM25",
        device_class=SensorDeviceClass.PM25,
        native_unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
        icon="mdi:chart-scatter-plot",
    ),
    SensorType.PM10: SensorEntityDescription(
        key=SensorType.PM10,
        name="PM10",
        device_class=SensorDeviceClass.PM10,
        native_unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
        icon="mdi:chart-scatter-plot-hexbin",
    ),
    SensorType.ILLUMINANCE: SensorEntityDescription(
        key=SensorType.ILLUMINANCE,
        name="Illuminance",
        device_class=SensorDeviceClass.ILLUMINANCE,
        native_unit_of_measurement=LIGHT_LUX,
        icon="mdi:weather-sunny",
    ),
    SensorType.HUMIDITY: SensorEntityDescription(
        key=SensorType.HUMIDITY,
        name="Humidity",
        device_class=SensorDeviceClass.HUMIDITY,
        native_unit_of_measurement=PERCENTAGE,
        icon="mdi:water-percent",
    ),
    SensorType.TEMPERATURE: SensorEntityDescription(
        key=SensorType.TEMPERATURE,
        name="Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        icon="mdi:thermometer",
    ),
    SensorType.TVOC: SensorEntityDescription(
        key=SensorType.TVOC,
        name="TVOC",
        device_class=None,  # SensorDeviceClass.VOLATILE_ORGANIC_COMPOUNDS_PARTS,
        native_unit_of_measurement=CONCENTRATION_PARTS_PER_BILLION,
        icon="mdi:air-filter",
    ),
    SensorType.IAQ: SensorEntityDescription(
        key=SensorType.IAQ,
        name="IAQ",
        device_class=SensorDeviceClass.AQI,
        native_unit_of_measurement="IAQ",
        icon="mdi:weather-windy",
    ),
}


class AirMonitorSensor(AirMonitorEntity, SensorEntity):
    """Air Monitor Sensor class."""

    def __init__(
        self,
        coordinator: AirMonitorDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
        sensor_key: str,
        entity_id: str,
    ):
        """Initialize the sensor class."""
        self._sensor_key = sensor_key
        self.entity_description = entity_description
        self.entity_id = entity_id
        super().__init__(coordinator)

    @property
    def unique_id(self) -> str | None:
        """Return a unique ID to use for this entity."""
        return f"{self.coordinator.data['device_id']}_{self._sensor_key}"

    @property
    def native_value(self) -> str:
        """Return the native state of the sensor."""
        return self.coordinator.data["sensors"][self._sensor_key]
