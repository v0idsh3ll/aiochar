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

        return Post(**raw)

    async def get_user_posts(
            self,
            user_id: int,
            limit: int,
            ids_only: bool = False) -> tuple[Post] | tuple[int]:
        """
        Abstract (not the raw API) method to get user posts by limit

        :param user_id: User's ID. May be here: https://char.social/u/USER_ID
        :param limit: Limit to get posts. Get last LIMIT posts.
        :param ids_only: Return only post ids without any other data
        :return: Tuple of user posts
        """
        got_posts = 0

        before_id = None

        returned_data = []

        posts = await self.session.get(path=f"user_feed/{user_id}?ids_only={'true' if ids_only else 'false'}")
        before_id = posts["next_before_id"]
        if ids_only:
            for post_id in posts["posts"]:
                if got_posts >= limit:
                    return tuple(returned_data)
                returned_data.append(post_id)
                got_posts += 1
        else:
            for post_data in posts["posts"]:
                if got_posts >= limit:
                    return tuple(returned_data)
                returned_data.append(Post(**post_data))
                got_posts += 1

        has_more = posts["has_more"]
        while got_posts < limit and has_more:
            posts = await self.session.get(path=f"user_feed/{user_id}?ids_only={'true' if ids_only else 'false'}&before_id={before_id}")
            before_id = posts["next_before_id"]
            has_more = posts["has_more"]
            if ids_only:
                for post_id in posts["posts"]:
                    if got_posts >= limit:
                        return tuple(returned_data)
                    returned_data.append(post_id)
                    got_posts += 1
            else:
                for post_data in posts["posts"]:
                    if got_posts >= limit:
                        return tuple(returned_data)
                    returned_data.append(Post(**post_data))
                    got_posts += 1

        return tuple(returned_data)


    #POST METHODS

    # async def like_post(
    #         self,
    #         post: Post | None = None,
    #         post_id: int | None = None) -> dict:
    #     """
    #     Like a post by id
    #
    #     :param post: Post you can get by Bot.post() or similar
    #     :param post_id: Post_id, int
    #     :return: like_count, liked, post_id, success
    #     :raise: NotFoundPost when not found post API error, NoEnoughData when no post and no post_id
    #     """
    #     if not post and not post_id:
    #         raise NoEnoughData
    #
    #     data = {
    #         "post_id": post_id
    #     }
    #
    #     raw = await self.session.post(path="like_post", data=data)
    #
    #     return raw

    # NOT THE AIOHTTP METHODS

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