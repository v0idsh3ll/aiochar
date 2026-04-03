import aiohttp

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
        async with session.get(url=f"https://char.social/api/v1/{path.lstrip('/')}", **kwargs) as response:
            return await response.json()