"""Constants for acer_air_monitor tests."""
from custom_components.acer_air_monitor.const import (
    CONF_EMAIL,
    CONF_PASSWORD,
    USER_ATTR,
)

MOCK_CONFIG = {CONF_EMAIL: "test_email", CONF_PASSWORD: "test_password"}

MOCK_USER_CONFIG = {
    USER_ATTR: {
        "accessToken": "test_access_token",
        "aopUserId": "test_user_id",
        "createdDatetime": "2021-09-23 13:39:44",
        "email": "test_email",
        "id": "1234",
        "name": "test_name",
        "regToken": "",
        "status": "y",
        "updatedDatetime": "2021-09-23 13:39:44",
        "web_auth_name": "test_auth_name",
    }
}

MOCK_LOGIN_RESPONSE = {
    "data": MOCK_USER_CONFIG[USER_ATTR],
    "description": "RET_OK",
    "ret": "RET_OK",
}

MOCK_DEVICE = {
    "aopDeviceId": "test_aop_device_id",
    "battery": {"batteryLevel": 100, "isCharging": True},
    "bleMac": "00:11:22:33:44:55",
    "createdDatetime": 1632405330,
    "device_id": "12345",
    "historyFrom": "1632405300",
    "latestBleVersion": "acer_AM100_V2.03",
    "mac": "00:11:22:33:44:55",
    "modelName": "AM100",
    "name": "Acer Air Monitor",
    "sensors": {
        "co2": "700",
        "hum": "76",
        "iaq": "31",
        "lux": "1",
        "pm100": "1",
        "pm25": "1",
        "temp": "24.14",
        "tick": 1632406560,
        "tvoc": "194",
    },
    "status": "y",
}

MOCK_GET_DEVICES_RESPONSE = {
    "data": [MOCK_DEVICE],
    "ret": "RET_OK",
    "retDescription": "RET_OK",
}
