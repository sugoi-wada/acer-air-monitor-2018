"""Acer Air Monitor API Client."""
from abc import ABC
import logging

import aiohttp
from aiohttp.formdata import FormData
import async_timeout

from .const import BASE_URL

TIMEOUT = 10

_LOGGER: logging.Logger = logging.getLogger(__package__)

HEADERS = {"Content-type": "application/json; charset=UTF-8"}


def tryApiWrapper(func):
    async def wrapper_call(*args, **kwargs):
        try:
            async with async_timeout.timeout(TIMEOUT):
                return await func(*args, **kwargs)
        except (Exception,) as exception:
            _LOGGER.info(exception)
            return {}

    return wrapper_call


class BaseApiClient(ABC):
    def __init__(self, session: aiohttp.ClientSession) -> None:
        """Air Monitor API Client."""
        self._session = session


class AirMonitorAuthApiClient(BaseApiClient):
    def __init__(
        self, email: str, password: str, session: aiohttp.ClientSession
    ) -> None:
        """Air Monitor Auth API Client."""
        self._email = email
        self._password = password
        super().__init__(session)

    @tryApiWrapper
    async def login(self) -> dict:
        """Login with email."""
        url = f"{BASE_URL}/user/services/login.php"
        form = FormData()
        form.add_field("email", self._email)
        form.add_field("password", self._password)
        response = await self._session.post(url, data=form)
        return await response.json()


class AirMonitorApiClient(BaseApiClient):
    def __init__(self, userId: str, session: aiohttp.ClientSession) -> None:
        """Air Monitor API Client."""
        self._userId = userId
        super().__init__(session)

    @tryApiWrapper
    async def get_devices(self) -> dict:
        """Get devices."""
        url = f"{BASE_URL}/airmentor/query.php?user_id={self._userId}"
        response = await self._session.get(url)
        return await response.json()
