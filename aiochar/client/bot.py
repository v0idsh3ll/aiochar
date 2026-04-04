from aiochar.utils.token import validate_token
from .session.base import BaseSession
from ..exceptions import InvalidKey, NotFoundPost, NoEnoughData, APIError
from ..models import Post


class Bot:
    def __init__(
            self,
            token: str,
            session: BaseSession | None = None):
        """
        Bot class.

        :param token: Char Bot token `Obtained from profile editor <https://char.social/ID_HERE>`_
        :raise TokenValidationError: When token has invalid format this exception will be raised
        """

        validate_token(token)

        self._own_session = session is None

        self.__token = token
        self.base_headers = {"Authorization": f"Bearer {token}"}

        self.session = session or BaseSession(base_headers=self.base_headers)

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
        me_id = await self.session.get(path="me")

        return me_id["user_id"]

    async def get_post(
             self,
             post_id: int) -> Post:
        """
        Get Post and its data by post_id

        :param post_id: Post's for getting ID
        :return: Post with returned data
        """
        raw = await self.session.get(path=f"post/{post_id}")

        params = ("id", "user_id", "username", "api_bot", "flair", "content", "content_html", "created_at_iso", "country_code", "like_post_id", "like_count", "reply_count", "repost_count", "is_liked", "is_own_post", "hashtags", "mentions", "repost_of_id", "repost_text")

        data = {key: raw["post"][key] for key in params}
        data["post_id"] = data.pop("id")
        return Post(**data)


    #POST METHODS

    async def like_post(
            self,
            post: Post | None = None,
            post_id: int | None = None) -> dict:
        """
        Like a post by id

        :param post: Post you can get by Bot.post() or similar
        :param post_id: Post_id, int
        :return: like_count, liked, post_id, success
        :raise: NotFoundPost when not found post API error, NoEnoughData when no post and no post_id
        """
        if not post and not post_id:
            raise NoEnoughData

        data = {
            "post_id": post_id
        }

        raw = await self.session.post(path="like_post", data=data)

        return raw


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