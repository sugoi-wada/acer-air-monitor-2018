"""Constants for acer_air_monitor."""
from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

MANUFACTURER = "Acer"
NAME = f"{MANUFACTURER} Air Monitor"
DOMAIN = "acer_air_monitor"
VERSION = "1.2.0"
ATTRIBUTION = "Data provided by Acer Air Monitor"

# for Acer User configuration
USER_ATTR = "user_attr"
USER_ID = "aopUserId"
