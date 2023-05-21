"""Acer Air Monitor API Client."""
from __future__ import annotations

from abc import ABC

import asyncio
import socket

import aiohttp
import async_timeout
from aiohttp.formdata import FormData


from .const import BASE_URL

TIMEOUT = 10

# _LOGGER: logging.Logger = logging.getLogger(__package__)

HEADERS = {"Content-type": "application/json; charset=UTF-8"}


class ClientError(Exception):
    """Exception to indicate a general API error."""


class ClientCommunicationError(ClientError):
    """Exception to indicate a communication error."""


class ClientAuthenticationError(ClientError):
    """Exception to indicate an authentication error."""


def try_api_wrapper(func):
    """Wrap API calls with a try catch."""

    async def wrapper_call(*args, **kwargs):
        try:
            async with async_timeout.timeout(TIMEOUT):
                ret = await func(*args, **kwargs)
        except asyncio.TimeoutError as exception:
            raise ClientCommunicationError(
                "Timeout error fetching information",
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            raise ClientCommunicationError(
                "Error fetching information",
            ) from exception
        except Exception as exception:  # pylint: disable=broad-except
            raise ClientError("Something really wrong happened!") from exception
        else:
            if ret["ret"] != "RET_OK":
                raise ClientError(
                    f"Error fetching information: {ret['retDescription']}"
                )
            return ret

    return wrapper_call


class BaseApiClient(ABC):
    """Base API Client."""

    def __init__(self, session: aiohttp.ClientSession) -> None:
        """Air Monitor API Client."""
        self._session = session


class AirMonitorAuthApiClient(BaseApiClient):
    """Air Monitor Auth API Client."""

    def __init__(
        self, email: str, password: str, session: aiohttp.ClientSession
    ) -> None:
        """Air Monitor Auth API Client."""
        self._email = email
        self._password = password
        super().__init__(session)

    @try_api_wrapper
    async def login(self) -> dict:
        """Login with email."""
        url = f"{BASE_URL}/user/services/login.php"
        form = FormData()
        form.add_field("email", self._email)
        form.add_field("password", self._password)
        response = await self._session.post(url, data=form)
        if response.status in (401, 403):
            raise ClientAuthenticationError("Invalid credentials")
        response.raise_for_status()
        return await response.json()


class AirMonitorApiClient(BaseApiClient):
    """Air Monitor API Client."""

    def __init__(self, user_id: str, session: aiohttp.ClientSession) -> None:
        """Air Monitor API Client."""
        self._user_id = user_id
        super().__init__(session)

    @try_api_wrapper
    async def get_devices(self) -> dict:
        """Get devices."""
        url = f"{BASE_URL}/airmentor/query.php?user_id={self._user_id}"
        response = await self._session.get(url)
        if response.status in (401, 403):
            raise ClientAuthenticationError("Invalid credentials")
        response.raise_for_status()
        return await response.json()
