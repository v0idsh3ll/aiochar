from aiochar.utils.token import validate_token
from .session.base import BaseSession
from ..exceptions import InvalidKey, NotFoundPost


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

    #GET METHODS
    async def get_me(self) -> int:
        """
        Get id by token.

        :return: Profile's ID
        :raise: InvalidKey when invalid_api_key API error
        """
        me_id = await self.session.get(path="me", headers=self.base_headers)

        if "user_id" in me_id:
            return me_id["user_id"]
        elif "error" in me_id:
            if me_id["error"]["code"] == "invalid_api_key":
                raise InvalidKey
            else:
                raise Exception(me_id["message"])


    #POST METHODS

    async def like_post(
            self,
            post_id: int
    ) -> dict:
        """
        Like a post by id

        :param post_id: Post_id, int
        :return: like_count, liked, post_id, success
        :raise: NotFoundPost when not found post API error, InvalidKey when invalid_api_key
        """
        data = {
            "post_id": post_id
        }

        raw = await self.session.post(path="like_post", headers=self.base_headers, data=data)

        if "error" in raw:
            if raw["error"]["code"] == "not_found":
                raise NotFoundPost
            elif raw["error"]["code"] == "invalid_api_key":
                raise InvalidKey
            else:
                raise Exception(raw["error"]["code"])
        else:
            returned_data = {
                "like_count": raw["like_count"],
                "liked": raw["liked"],
                "post_id": raw["post_id"],
                "success": raw["success"]
            }
            return returned_data


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