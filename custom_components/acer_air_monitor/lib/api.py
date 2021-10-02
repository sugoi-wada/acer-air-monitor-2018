"""Acer Air Monitor API Client."""
from abc import ABC
import asyncio
import logging
import socket
from typing import Optional

from aiohttp.formdata import FormData
from .const import BASE_URL

import aiohttp
import async_timeout

TIMEOUT = 10

_LOGGER: logging.Logger = logging.getLogger(__package__)

HEADERS = {"Content-type": "application/json; charset=UTF-8"}


def tryApiWrapper(func):
    async def wrapper_call(*args, **kwargs):
        try:
            async with async_timeout.timeout(TIMEOUT, loop=asyncio.get_event_loop()):
                return await func(*args, **kwargs)
        except (Exception,) as exception:
            _LOGGER.info(exception)
            return {}

    return wrapper_call


class BaseApiClient(ABC):
    def __init__(self, session: aiohttp.ClientSession) -> None:
        """Air Monitor API Client."""
        self._session = session

    async def api_wrapper(
        self, method: str, url: str, data: dict = {}, headers: dict = {}
    ) -> Optional[dict]:
        """Get information from the API."""
        try:
            async with async_timeout.timeout(TIMEOUT, loop=asyncio.get_event_loop()):
                if method == "get":
                    response = await self._session.get(url, headers=headers)
                    return await response.json()

                elif method == "put":
                    await self._session.put(url, headers=headers, json=data)

                elif method == "patch":
                    await self._session.patch(url, headers=headers, json=data)

                elif method == "post":
                    response = await self._session.post(url, headers=headers, json=data)
                    return response

        except asyncio.TimeoutError as exception:
            _LOGGER.error(
                "Timeout error fetching information from %s - %s",
                url,
                exception,
            )

        except (KeyError, TypeError) as exception:
            _LOGGER.error(
                "Error parsing information from %s - %s",
                url,
                exception,
            )
        except (aiohttp.ClientError, socket.gaierror) as exception:
            _LOGGER.error(
                "Error fetching information from %s - %s",
                url,
                exception,
            )
        except Exception as exception:  # pylint: disable=broad-except
            _LOGGER.error("Something really wrong happened! - %s", exception)


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

    async def async_get_data(self) -> dict:
        """Get data from the API."""
        url = "https://jsonplaceholder.typicode.com/posts/1"
        return await self.api_wrapper("get", url)

    async def async_set_title(self, value: str) -> None:
        """Get data from the API."""
        url = "https://jsonplaceholder.typicode.com/posts/1"
        await self.api_wrapper("patch", url, data={"title": value}, headers=HEADERS)
