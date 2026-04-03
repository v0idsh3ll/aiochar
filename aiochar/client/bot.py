from aiochar.utils.token import validate_token
from .session.base import BaseSession
from ..exceptions import InvalidKey


class Bot:
    def __init__(
            self,
            token: str,
            session: BaseSession | None = None) -> None:
        """
        Bot class.

        :param token: Char Bot token `Obtained from profile editor <https://char.social/ID_HERE>`_
        :raise TokenValidationError: When token has invalid format this exception will be raised
        """

        validate_token(token)

        self._own_session = session is None
        self.session = session or BaseSession()

        self.__token = token
        self.base_headers = {"Authorization": f"Bearer {token}"}

    @property
    def token(self):
        return self.__token

    async def get_me(self) -> int:
        """
        Get id by token.

        :return: Profile's ID
        """
        me_id = await self.session.get(path="me", headers=self.base_headers)

        if me_id:
            if "user_id" in me_id:
                return me_id["user_id"]
            elif "error" in me_id:
                if me_id["error"]["code"] == "invalid_api_key":
                    raise InvalidKey


    async def close(self) -> None:
        """
        Method to close session and bot.

        :param self:
        :return:
        """
        if self._own_session:
            await self.session.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.close()