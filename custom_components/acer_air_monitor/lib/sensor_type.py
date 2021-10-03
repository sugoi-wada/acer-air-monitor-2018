from enum import Enum


class SensorType(str, Enum):
    CO2 = "co2"
    PM25 = "pm25"
    PM10 = "pm100"
    ILLUMINANCE = "lux"
    HUMIDITY = "hum"
    TEMPERATURE = "temp"
    TVOC = "tvoc"
    IAQ = "iaq"
