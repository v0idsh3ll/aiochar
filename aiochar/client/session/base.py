import aiohttp
from aiochar.exceptions import CharBadRequest, APIError, InvalidKey, NotFoundPost
from asyncio import sleep

def snake_to_camel(name: str) -> str:
    parts = name.split('_')
    return ''.join(word.capitalize() for word in parts)

class BaseSession:
    def __init__(
            self,
            base_url="https://char.social/api/v1/",
            base_headers=None):
        self.base_url = base_url
        self._session: aiohttp.ClientSession | None = None
        self._base_headers = base_headers

    async def get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session

    async def close(self):
        if self._session and not self._session.closed:
            await self._session.close()

    async def get(self,
                  path: str,
                  **kwargs) -> dict[str, ...]:
        """
        Get request
        :param path: Path after https://char.social/api/v1/
        :return: Response
        """
        session = await self.get_session()
        status = 0
        delay = 1
        while status == 503 or status == 0:
            await sleep(delay)
            delay = min(2 * delay, 60)
            async with session.get(url=f"{self.base_url}{path.lstrip('/')}", headers=self._base_headers, **kwargs) as response:
                status = response.status
                try:
                    json_format = await response.json()
                except Exception:
                    raise APIError("Invalid JSON response")

                if response.status == 400:
                    raise CharBadRequest
                if "error" in json_format:
                    code = json_format["error"]["code"]
                    if code == "invalid_api_key":
                        raise InvalidKey
                    elif code == "not_found":
                        raise NotFoundPost
                    else:
                        code = json_format["error"]["code"]
                        message = json_format["error"].get("message", "")

                        exc_name = snake_to_camel(code)
                        ExcCls = type(exc_name, (APIError,), {})
                        raise ExcCls(message)

                response.raise_for_status()
                return json_format

    async def post(self,
                  path: str,
                  **kwargs) -> dict[str, ...]:
        """
        Get request
        :param path: Path after https://char.social/api/v1/
        :return: Response
        """
        session = await self.get_session()
        status = 0
        delay = 1
        while status == 503 or status == 0:
            await sleep(delay)
            delay = min(2*delay, 60)
            async with session.post(url=f"{self.base_url}{path.lstrip('/')}", headers=self._base_headers, **kwargs) as response:
                status = response.status
                try:
                    json_format = await response.json()
                except Exception:
                    raise APIError("Invalid JSON response")

                if response.status == 400:
                    raise CharBadRequest
                if "error" in json_format:
                    code = json_format["error"]["code"]
                    if code == "invalid_api_key":
                        raise InvalidKey
                    elif code == "not_found":
                        raise NotFoundPost
                    else:
                        code = json_format["error"]["code"]
                        message = json_format["error"].get("message", "")

                        exc_name = snake_to_camel(code)
                        ExcCls = type(exc_name, (APIError,), {})
                        raise ExcCls(message)

                response.raise_for_status()
                return json_format