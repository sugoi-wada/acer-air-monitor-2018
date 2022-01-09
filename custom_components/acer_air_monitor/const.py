"""Constants for acer_air_monitor."""
# Base component constants
MANUFACTURER = "Acer"
NAME = f"{MANUFACTURER} Air Monitor"
DOMAIN = "acer_air_monitor"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "1.0.1"
ISSUE_URL = "https://github.com/sugoi-wada/acer-air-monitor-2018/issues"

# Icons
ICON = "mdi:format-quote-close"

# Platforms
SENSOR = "sensor"
PLATFORMS = [SENSOR]

# Configuration and options
CONF_ENABLED = "enabled"
CONF_EMAIL = "email"
CONF_PASSWORD = "password"

USER_ATTR = "user_attr"

USER_ID = "aopUserId"

STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""
