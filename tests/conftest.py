"""Global fixtures for acer_air_monitor integration."""
# Fixtures allow you to replace functions with a Mock object. You can perform
# many options via the Mock to reflect a particular behavior from the original
# function that you want to see without going through the function's actual logic.
# Fixtures can either be passed into tests as parameters, or if autouse=True, they
# will automatically be used across all tests.
#
# Fixtures that are defined in conftest.py are available across all tests. You can also
# define fixtures within a particular test file to scope them locally.
#
# pytest_homeassistant_custom_component provides some fixtures that are provided by
# Home Assistant core. You can find those fixture definitions here:
# https://github.com/MatthewFlamm/pytest-homeassistant-custom-component/blob/master/pytest_homeassistant_custom_component/common.py
#
# See here for more info: https://docs.pytest.org/en/latest/fixture.html (note that
# pytest includes fixtures OOB which you can use as defined on this page)
from unittest.mock import patch

import pytest

from tests.const import MOCK_GET_DEVICES_RESPONSE, MOCK_LOGIN_RESPONSE

pytest_plugins = "pytest_homeassistant_custom_component"


# This fixture enables loading custom integrations in all tests.
# Remove to enable selective use of this fixture
@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):
    yield


# This fixture is used to prevent HomeAssistant from attempting to create and dismiss persistent
# notifications. These calls would fail without this fixture since the persistent_notification
# integration is never loaded during a test.
@pytest.fixture(name="skip_notifications", autouse=True)
def skip_notifications_fixture():
    """Skip notification calls."""
    with patch("homeassistant.components.persistent_notification.async_create"), patch(
        "homeassistant.components.persistent_notification.async_dismiss"
    ):
        yield


@pytest.fixture(name="bypass_login")
def bypass_login_fixture():
    """Skip calls to login from API."""
    with patch(
        "custom_components.acer_air_monitor.lib.api.AirMonitorAuthApiClient.login",
        return_value=MOCK_LOGIN_RESPONSE,
    ):
        yield


@pytest.fixture(name="bypass_get_devices")
def bypass_get_devices_fixture():
    """Skip calls to get data from API."""
    with patch(
        "custom_components.acer_air_monitor.lib.api.AirMonitorApiClient.get_devices",
        return_value=MOCK_GET_DEVICES_RESPONSE,
    ):
        yield


@pytest.fixture(name="error_on_login")
def error_login_fixture():
    """Simulate error when login from API."""
    with patch(
        "custom_components.acer_air_monitor.lib.api.AirMonitorAuthApiClient.login",
        side_effect=Exception,
    ):
        yield


@pytest.fixture(name="error_on_get_devices")
def error_get_devices_fixture():
    """Simulate error when retrieving data from API."""
    with patch(
        "custom_components.acer_air_monitor.lib.api.AirMonitorApiClient.get_devices",
        side_effect=Exception,
    ):
        yield
