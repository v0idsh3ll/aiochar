import aiohttp
from aiochar.exceptions import CharBadRequest, APIError, InvalidKey, NotFound
from asyncio import sleep
from typing import Any, Dict, Optional
from aiolimiter import AsyncLimiter
import logging
logger = logging.getLogger('aiochar.session')
logger.addHandler(logging.NullHandler())

limiter = AsyncLimiter(120, 60)


def snake_to_camel(name: str) -> str:
    parts = name.split('_')
    return ''.join(word.capitalize() for word in parts)


class BaseSession:
    def __init__(
            self,
            base_url: str = "https://char.social/api/v1/",
            base_headers: Optional[Dict[str, str]] = None) -> None:
        self.base_url = base_url
        self._session: Optional[aiohttp.ClientSession] = None
        self._base_headers = base_headers
        self._429_delay: float = 1.0
        logger.info('Session was created')

    async def get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session."""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session

    async def close(self) -> None:
        """Close aiohttp session."""
        if self._session and not self._session.closed:
            await self._session.close()
            logger.debug('Session is closed')

    async def _request(self, method: str, path: str, **kwargs) -> Dict[str, Any]:
        """Send HTTP request to API endpoint with rate limiting and 429 handling.

        :param method: HTTP method (GET or POST)
        :param path: Path after https://char.social/api/v1/
        :return: JSON response as dictionary
        :raises APIError: When response is not valid JSON
        :raises InvalidKey: When API key is invalid
        :raises NotFoundPost: When post not found
        :raises CharBadRequest: When request is malformed
        """
        session = await self.get_session()

        async with limiter:
            logger.debug(f'Making request with method {method} and path {path}')
            try:
                async with session.request(
                    method=method,
                    url=f"{self.base_url}{path.lstrip('/')}",
                    headers=self._base_headers,
                    **kwargs
                ) as response:
                    if response.status == 429:
                        await sleep(self._429_delay)
                        self._429_delay = min(self._429_delay * 2, 60.0)
                        return await self._request(method, path, **kwargs)

                    self._429_delay = max(1.0, self._429_delay * 0.9)

                    try:
                        json_format = await response.json()
                    except Exception:
                        text = await response.text()
                        raise APIError(f"Non-JSON response ({response.status}): {text[:200]}")

                    if response.status == 400:
                        raise CharBadRequest

                    if "error" in json_format:
                        code = json_format["error"]["code"]
                        if code == "invalid_api_key":
                            raise InvalidKey
                        elif code == "not_found":
                            raise NotFound
                        else:
                            message = json_format["error"].get("message", "")
                            exc_name = snake_to_camel(code)
                            ExcCls = type(exc_name, (APIError,), {})
                            raise ExcCls(message)

                    response.raise_for_status()
                    return json_format
            except (aiohttp.ClientError, aiohttp.ConnectionTimeoutError):
                logger.error('Connection error')
                await sleep(self._429_delay)
                self._429_delay = min(self._429_delay * 2, 60.0)
                return await self._request(method, path, **kwargs)

    async def get(self, path: str, **kwargs) -> Dict[str, Any]:
        """Send GET request to API endpoint.

        :param path: Path after https://char.social/api/v1/
        :return: JSON response as dictionary
        :raises APIError: When response is not valid JSON
        :raises InvalidKey: When API key is invalid
        :raises NotFoundPost: When post not found
        :raises CharBadRequest: When request is malformed
        """
        return await self._request("GET", path, **kwargs)

    async def post(self, path: str, **kwargs) -> Dict[str, Any]:
        """Send POST request to API endpoint.

        :param path: Path after https://char.social/api/v1/
        :return: JSON response as dictionary
        :raises APIError: When response is not valid JSON
        :raises InvalidKey: When API key is invalid
        :raises NotFoundPost: When post not found
        :raises CharBadRequest: When request is malformed
        """
        return await self._request("POST", path, **kwargs)