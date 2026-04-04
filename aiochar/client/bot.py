from typing import List

from aiochar.utils.token import validate_token
from .session.base import BaseSession
from ..exceptions import InvalidKey, NotFoundPost, NoEnoughData, APIError
from ..models import Post, User, Reply

from .utils import sort_validation, timeframe_validation


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

    async def get_user_replies(
            self,
            user_id: int,
            limit: int,
            ids_only: bool = False) -> tuple[Post] | tuple[int]:
        """
        Abstract (not the raw API) method to get user replies by limit

        :param user_id: User's ID. May be here: https://char.social/u/USER_ID
        :param limit: Limit to get posts. Get last LIMIT posts.
        :param ids_only: Return only post ids without any other data
        :return: Tuple of user posts
        """
        got_posts = 0

        before_id = None

        returned_data = []

        posts = await self.session.get(path=f"user_replies_feed/{user_id}?ids_only={'true' if ids_only else 'false'}")
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
                returned_data.append(Reply(**post_data))
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
                    returned_data.append(Reply(**post_data))
                    got_posts += 1

        return tuple(returned_data)

    async def get_hashtag_feed(
            self,
            hashtag: str,
            limit: int = 1,
            sort: str = "latest",
            timeframe: str = "24h",
            ids_only: bool = False) -> List[Post, Reply] | List[Post] | List[Reply]:
        """
        Abstract (not the raw API) method to get hashtag feed posts by limit

    Gets posts from a specific hashtag feed with pagination support.
    Uses cursor-based pagination internally to fetch exactly `limit` posts.

    :param hashtag: Hashtag to fetch posts from (without the # symbol)
    :param limit: Maximum number of posts to retrieve. Gets last LIMIT posts.
    :param sort: Sort order for posts. Options: "latest", "popular", "likes". Default: "latest"
    :param timeframe: Time window for sorting by likes. Options: "24h", "1w", "1m", "1y", "all".
                      Only applies when sort="likes". Default: "24h"
    :param ids_only: Return only post IDs without any other data. If True, returns tuple of ints.
                     If False, returns tuple of Post/Reply objects.
    :return: Tuple of posts (Post/Reply objects if ids_only=False) or tuple of post IDs (ints if ids_only=True)
        """
        if sort:
            sort_validation(sort)
        if timeframe:
            timeframe_validation(timeframe)

        got_posts = 0

        returned_data = []

        posts = await self.session.get(path=f"hashtag_feed/{hashtag}?ids_only={'true' if ids_only else 'false'}")
        cursor = posts["next_cursor"]
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
            posts = await self.session.get(
                path=f"hashtag_feed/{hashtag}?ids_only={'true' if ids_only else 'false'}&cursor={cursor}")
            cursor = posts["next_cursor"]
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

    async def get_user(
            self,
            user_id: int) -> User:
        """
        Get a user by id

        :param user_id: User's ID. May be here: https://char.social/u/USER_ID
        :return: User
        """
        raw = await self.session.get(path=f"user/{user_id}")
        raw = raw["user"]

        counted = {**raw["counts"]}

        user_data = {**raw}
        user_data.pop("counts")

        user_data.update(**counted)

        return User(**user_data)



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