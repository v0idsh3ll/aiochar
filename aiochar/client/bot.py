import asyncio
from typing import List

from aiochar.utils.token import validate_token
from .session.base import BaseSession
from ..models import Post, User, Reply, Hashtag

from .utils import sort_validation, timeframe_validation, country_code_validation, post_format_validation, post_content_validation, leaderboard_category_validation

from ..exceptions import NoEnoughData


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
             post_id: int) -> Post | Reply:
        """
        Get Post and its data by post_id

        :param post_id: Post's for getting ID
        :return: Post with returned data
        """
        raw = await self.session.get(path=f"post/{post_id}")

        raw = raw["post"]

        return Post(**raw) if not "parent_post_id" in raw else Reply(**raw)

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
            hashtag: str | Hashtag,
            limit: int = 1,
            sort: str = "latest",
            timeframe: str = "24h",
            ids_only: bool = False) -> tuple[Post | Reply, ...] | tuple[int, ...]:
        """
        Abstract (not the raw API) method to get hashtag feed posts by limit

    Gets posts from a specific hashtag feed with pagination support.
    Uses cursor-based pagination internally to fetch exactly `limit` posts.

    :param hashtag: Hashtag to fetch posts from
    :param limit: Maximum number of posts to retrieve. Gets last LIMIT posts.
    :param sort: Sort order for posts. Options: "latest", "popular", "likes". Default: "latest"
    :param timeframe: Time window for sorting by likes. Options: "24h", "1w", "1m", "1y", "all".
                      Only applies when sort="likes". Default: "24h"
    :param ids_only: Return only post IDs without any other data. If True, returns tuple of ints.
                     If False, returns tuple of Post/Reply objects.
    :return: Tuple of posts (Post/Reply objects if ids_only=False) or tuple of post IDs (ints if ids_only=True)
        """

        # MAKE POST AND REPLIES VALIDATION AND RETURN CORRECT VERSIONS

        if sort:
            sort_validation(sort)
        if timeframe:
            timeframe_validation(timeframe)

        hashtag = hashtag.lstrip("#")

        got_posts = 0

        returned_data = []

        posts = await self.session.get(path=f"hashtag_feed/{hashtag}?ids_only={'true' if ids_only else 'false'}&sort={sort or 'latest'}&timeframe={timeframe or ''}")
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
                path=f"hashtag_feed/{hashtag}?ids_only={'true' if ids_only else 'false'}&cursor={cursor}&sort={sort or 'latest'}&timeframe={timeframe or ''}")
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

    async def get_feed(
            self,
            limit: int = 1,
            sort: str = "latest",
            timeframe: str = "24h",
            ids_only: bool = False) -> tuple[Post | Reply, ...] | tuple[int, ...]:
        """
        Abstract (not the raw API) method to get hashtag feed posts by limit

    Gets posts from a specific hashtag feed with pagination support.
    Uses cursor-based pagination internally to fetch exactly `limit` posts.

    :param limit: Maximum number of posts to retrieve. Gets last LIMIT posts.
    :param sort: Sort order for posts. Options: "latest", "popular", "likes". Default: "latest"
    :param timeframe: Time window for sorting by likes. Options: "24h", "1w", "1m", "1y", "all".
                      Only applies when sort="likes". Default: "24h"
    :param ids_only: Return only post IDs without any other data. If True, returns tuple of ints.
                     If False, returns tuple of Post/Reply objects.
    :return: Tuple of posts (Post/Reply objects if ids_only=False) or tuple of post IDs (ints if ids_only=True)
        """

        # MAKE POST AND REPLIES VALIDATION AND RETURN CORRECT VERSIONS

        if sort:
            sort_validation(sort)
        if timeframe:
            timeframe_validation(timeframe)

        got_posts = 0

        returned_data = []

        posts = await self.session.get(path=f"feed?ids_only={'true' if ids_only else 'false'}&sort={sort or 'latest'}&timeframe={timeframe or ''}")
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
                path=f"feed?ids_only={'true' if ids_only else 'false'}&cursor={cursor}&sort={sort or 'latest'}&timeframe={timeframe or ''}")
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

    async def get_country_feed(
            self,
            country_code: str,
            limit: int = 1,
            sort: str = "latest",
            timeframe: str = "24h",
            ids_only: bool = False) -> tuple[Post | Reply, ...] | tuple[int, ...]:
        """
        Abstract (not the raw API) method to get hashtag feed posts by limit

    Gets posts from a specific hashtag feed with pagination support.
    Uses cursor-based pagination internally to fetch exactly `limit` posts.

    :param country_code: Country code to fetch posts from (RU/US/FR/etc)
    :param limit: Maximum number of posts to retrieve. Gets last LIMIT posts.
    :param sort: Sort order for posts. Options: "latest", "popular", "likes". Default: "latest"
    :param timeframe: Time window for sorting by likes. Options: "24h", "1w", "1m", "1y", "all".
                      Only applies when sort="likes". Default: "24h"
    :param ids_only: Return only post IDs without any other data. If True, returns tuple of ints.
                     If False, returns tuple of Post/Reply objects.
    :return: Tuple of posts (Post/Reply objects if ids_only=False) or tuple of post IDs (ints if ids_only=True)
        """

        # MAKE POST AND REPLIES VALIDATION AND RETURN CORRECT VERSIONS

        if sort:
            sort_validation(sort)
        if timeframe:
            timeframe_validation(timeframe)
        if country_code:
            country_code_validation(country_code)

        got_posts = 0

        returned_data = []

        posts = await self.session.get(path=f"country_feed/{country_code}?ids_only={'true' if ids_only else 'false'}&sort={sort or 'latest'}&timeframe={timeframe or ''}")
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
                path=f"country_feed/{country_code}?ids_only={'true' if ids_only else 'false'}&cursor={cursor}&sort={sort or 'latest'}&timeframe={timeframe or ''}")
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

    async def get_leaderboard(
            self,
            category: str,
            limit: int = 25,
            offset: int = 0) -> dict[str, int] | dict[User, int]:
        """
        Get leaderboard by category

        :param category: Category to get lb. Available: 'posts','likes','reposts','followers','mutes','followed_tags','muted_tags'.
        :param limit: Limit. Limit by values to return. Defaults to 25.
        :param offset: Number of items to skip for pagination. Defaults to 0.
        :return: dict like {User: int (how many)} or {str: int}.
        """
        leaderboard_category_validation(category)

        raw = await self.session.get(path=f"leaderboard?category={category}&offset={offset}&limit={limit}")

        if category.endswith('tags'):
            tags = {}
            for value in raw["users"]:
                tags[Hashtag(value["id"])] = value["count"]
            return tags

        else:
            users = {}
            for value in raw["users"]:
                user = await self.get_user(user_id=value["id"])
                users[user] = value["count"]
            return users

    async def get_following(
            self,
            limit: int = 1,
            user_id: int | None = None,
            user: User | None = None) -> tuple[User, ...]:
        """
        Get users who user follows.

        :param limit: Maximum number of users to retrieve. Gets last LIMIT users. 1 by default
        :param user_id: user_id of user you want to get followings
        :param user: User you want to get followings
        :return: Tuple of users who provided user follows
        """
        if not user and not user_id:
            raise NoEnoughData

        if user:
            user_id = user.id

        raw = await self.session.get(path=f"user/{user_id}/following?limit={limit}")
        users = []

        for user_ in raw["users"]:
            users.append(await self.get_user(user_))

        return tuple(users)

    async def get_followers(
            self,
            limit: int = 1,
            user_id: int | None = None,
            user: User | None = None) -> tuple[User, ...]:
        """
        Get users who are followed to a user.

        :param limit: Maximum number of users to retrieve. Gets last LIMIT users. 1 by default
        :param user_id: user_id of user you want to get followers
        :param user: User you want to get followers
        :return: Tuple of users who followed to provided user
        """
        if not user and not user_id:
            raise NoEnoughData

        if user:
            user_id = user.id

        raw = await self.session.get(path=f"user/{user_id}/followers?limit={limit}")
        users = []

        for user_ in raw["users"]:
            users.append(await self.get_user(user_))

        return tuple(users)

    async def get_muting(
            self,
            limit: int = 1,
            user_id: int | None = None,
            user: User | None = None) -> tuple[User, ...]:
        """
        Get users who user mutes.

        :param limit: Maximum number of users to retrieve. Gets last LIMIT users. 1 by default
        :param user_id: user_id of user you want to get mutes
        :param user: User you want to get mutes
        :return: Tuple of users who provided user mutes
        """
        if not user and not user_id:
            raise NoEnoughData

        if user:
            user_id = user.id

        raw = await self.session.get(path=f"user/{user_id}/muting?limit={limit}")
        users = []

        for user_ in raw["users"]:
            users.append(await self.get_user(user_))

        return tuple(users)

    async def get_muted_by(
            self,
            limit: int = 1,
            user_id: int | None = None,
            user: User | None = None) -> tuple[User, ...]:
        """
        Get users who muted a user.

        :param limit: Maximum number of users to retrieve. Gets last LIMIT users. 1 by default
        :param user_id: user_id of user you want to get muters
        :param user: User you want to get muters
        :return: Tuple of users who mutes provided user
        """
        if not user and not user_id:
            raise NoEnoughData

        if user:
            user_id = user.id

        raw = await self.session.get(path=f"user/{user_id}/muted_by?limit={limit}")
        users = []

        for user_ in raw["users"]:
            users.append(await self.get_user(user_))

        return tuple(users)

    async def get_followed_tags(
            self,
            limit: int = 1,
            user_id: int | None = None,
            user: User | None = None) -> tuple[Hashtag, ...]:
        """
        Get tags a user follows

        :param limit: Maximum number of tags to retrieve. Gets last LIMIT users. 1 by default
        :param user_id: user_id of user you want to get followed tags
        :param user: User you want to get followed tags
        :return: Tuple with Hashtags
        """
        if not user and not user_id:
            raise NoEnoughData

        if user:
            user_id = user.id

        raw = await self.session.get(path=f"user/{user_id}/followed_tags?limit={limit}")
        tags = []

        for tag in raw["tags"]:
            tags.append(Hashtag(tag))

        return tuple(tags)

    async def get_muted_tags(
            self,
            limit: int = 1,
            user_id: int | None = None,
            user: User | None = None) -> tuple[Hashtag, ...]:
        """
        Get tags a user mutes

        :param limit: Maximum number of tags to retrieve. Gets last LIMIT users. 1 by default
        :param user_id: user_id of user you want to get muted tags
        :param user: User you want to get muted tags
        :return: Tuple with Hashtags
        """
        if not user and not user_id:
            raise NoEnoughData

        if user:
            user_id = user.id

        raw = await self.session.get(path=f"user/{user_id}/muted_tags?limit={limit}")
        tags = []

        for tag in raw["tags"]:
            tags.append(Hashtag(tag))

        return tuple(tags)

    #POST METHODS

    async def create_post(
            self,
            content: str = "",
            poll_options: list[str] | tuple[str, ...] = ()
    ) -> Post:
        """
        Create a post (not reply or repost)

        :param content: Text of post. Max: 1024 symbols.
        :param poll_options: Poll_options. Max: 200 symbols for poll option content and max 4 poll options.
        :return: Post with created post data
        """
        post_format_validation(content, poll_options)

        data = {"content": content, "poll_options": poll_options}

        created_post_data = await self.session.post(path="post", json=data)
        created_post_id = created_post_data["post_id"]

        created_post = await self.get_post(created_post_id)

        return created_post

    async def create_reply(
            self,
            content: str,
            post: Post | None = None,
            post_id: int | None = None) -> Reply:
        """
        Reply to a post by id or Post()

        :param content: Text of reply. Max: 1024 symbols.
        :param post: Post() can be obtained with get_post or get feeds methods
        :param post_id: Integer with post ID
        :return: Reply() with reply data
        """
        post_content_validation(content)

        if not post and not post_id:
            raise NoEnoughData

        if post:
            post_id = post.id

        data = {"content": content}
        created_reply = await self.session.post(f"post/{post_id}/reply", json=data)
        created_reply_id = created_reply["post_id"]
        created_reply = await self.get_post(created_reply_id)

        return created_reply




    async def follow_user(
            self,
            user: User | None = None,
            user_id: int | None = None) -> bool:
        """
        Follow user by user_id or User()

        :param user: User()
        :param user_id: user_id
        :return: True if followed else False
        """
        if not user and not user_id:
            raise NoEnoughData

        if user:
            user_id = user.id

        data = {"user_id": user_id}

        followed = await self.session.post("follow_user", json=data)
        return followed["success"]

    async def unfollow_user(
            self,
            user: User | None = None,
            user_id: int | None = None) -> bool:
        """
        Unfollow user by user_id or User()

        :param user: User()
        :param user_id: user_id
        :return: True if followed else False
        """
        if not user and not user_id:
            raise NoEnoughData

        if user:
            user_id = user.id

        data = {"user_id": user_id}

        followed = await self.session.post("unfollow_user", json=data)
        return followed["success"]

    async def mute_user(
            self,
            user: User | None = None,
            user_id: int | None = None) -> bool:
        """
        Mute user by user_id or User()

        :param user: User()
        :param user_id: user_id
        :return: True if followed else False
        """
        if not user and not user_id:
            raise NoEnoughData

        if user:
            user_id = user.id

        data = {"user_id": user_id}

        followed = await self.session.post("mute_user", json=data)
        return followed["success"]

    async def unmute_user(
            self,
            user: User | None = None,
            user_id: int | None = None) -> bool:
        """
        Unmute user by user_id or User()

        :param user: User()
        :param user_id: user_id
        :return: True if followed else False
        """
        if not user and not user_id:
            raise NoEnoughData

        if user:
            user_id = user.id

        data = {"user_id": user_id}

        followed = await self.session.post("unmute_user", json=data)
        return followed["success"]

    async def follow_hashtag(
            self,
            hashtag: str | Hashtag) -> bool:
        if isinstance(hashtag, Hashtag):
            hashtag = hashtag.tag

        data = {"hashtag": hashtag}

        raw = await self.session.post(path="follow_tag", json=data)

        return raw["success"]

    async def unfollow_hashtag(
            self,
            hashtag: str | Hashtag) -> bool:
        if isinstance(hashtag, Hashtag):
            hashtag = hashtag.tag

        data = {"hashtag": hashtag}

        raw = await self.session.post(path="unfollow_tag", json=data)

        return raw["success"]

    async def mute_hashtag(
            self,
            hashtag: str | Hashtag) -> bool:
        if isinstance(hashtag, Hashtag):
            hashtag = hashtag.tag

        data = {"hashtag": hashtag}

        raw = await self.session.post(path="mute_tag", json=data)

        return raw["success"]

    async def unmute_hashtag(
            self,
            hashtag: str | Hashtag) -> bool:
        if isinstance(hashtag, Hashtag):
            hashtag = hashtag.tag

        data = {"hashtag": hashtag}

        raw = await self.session.post(path="unmute_tag", json=data)

        return raw["success"]

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