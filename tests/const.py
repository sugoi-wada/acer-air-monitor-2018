"""Constants for acer_air_monitor tests."""
from custom_components.acer_air_monitor.const import (
    CONF_PASSWORD,
    CONF_EMAIL,
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
