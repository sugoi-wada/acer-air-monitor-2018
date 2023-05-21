"""Sensor type."""
from enum import Enum


class SensorType(str, Enum):
    """Sensor type."""

    CO2 = "co2"
    PM25 = "pm25"
    PM10 = "pm100"
    ILLUMINANCE = "lux"
    HUMIDITY = "hum"
    TEMPERATURE = "temp"
    TVOC = "tvoc"
    IAQ = "iaq"
