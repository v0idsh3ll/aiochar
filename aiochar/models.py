from datetime import datetime


class Post:
    def __init__(
        self,
        id: int,
        user_id: int,
        username: str,
        api_bot: bool,
        flair: list[str],
        content: str,
        content_html: str,
        created_at_iso: str,
        country_code: str,
        like_post_id: int,
        like_count: int,
        reply_count: int,
        repost_count: int,
        is_liked: bool,
        is_own_post: bool,
        hashtags: list[str],
        mentions: list[str],
        repost_of_id: int | None = None,
        repost_text: str | None = None,
        **kwargs) -> None:

        for key, value in kwargs.items():
            setattr(self, key, value)

        self.id = int(id)
        self.user_id = int(user_id)
        self.username = str(username)

        self.api_bot = bool(api_bot)
        self.flair = flair or []

        self.content = content or ""
        self.content_html = content_html or ""

        try:
            self.created_at_iso = datetime.fromisoformat(created_at_iso.replace("Z", "+00:00"))
        except Exception:
            self.created_at_iso = None

        self.country_code = country_code or "??"

        self.like_post_id = like_post_id

        self.like_count = int(like_count or 0)
        self.reply_count = int(reply_count or 0)
        self.repost_count = int(repost_count or 0)

        self.is_liked = bool(is_liked)
        self.is_own_post = bool(is_own_post)

        self.hashtags = hashtags or []
        self.mentions = mentions or []

        self.repost_of_id = repost_of_id
        self.repost_text = repost_text

    def to_dict(self) -> dict:
        """
        Convert a post to a dict

        :return: Dict with post data
        """
        result = self.__dict__.copy()
        if result.get("created_at_iso"):
            result["created_at_iso"] = result["created_at_iso"].isoformat()
        return result

    def __str__(self):
        return str(self.to_dict())


class User:
    """
    Main class to contain users
    """
    def __init__(
            self,
            id: int,
            username: str,
            flair: list[str],
            created_at_iso: str,
            api_bot: bool,
            followed: bool,
            muted: bool,
            followers: int,
            following: int,
            muting: int,
            muted_by: int,
            followed_tags: int,
            muted_tags: int,
            posts: int,
            post_posts: int,
            post_reposts: int,
            post_replies: int,
            likes_received: int,
            description: str = "",
            **kwargs):

        for key, value in kwargs.items():
            setattr(self, key, value)

        self.id = id
        self.username = username
        self.flair = flair

        try:
            self.created_at_iso = datetime.fromisoformat(created_at_iso.replace("Z", "+00:00"))
        except Exception:
            self.created_at_iso = None

        self.api_bot = api_bot
        self.followed = followed
        self.muted = muted
        self.followers = followers
        self.following = following
        self.muting = muting
        self.muted_by = muted_by
        self.followed_tags = followed_tags
        self.muted_tags = muted_tags
        self.posts = posts
        self.post_posts = post_posts
        self.post_reposts = post_reposts
        self.post_replies = post_replies
        self.likes_received = likes_received
        self.description = description

    def to_dict(self) -> dict:
        """
        Convert a user to a dict

        :return: Dict with user data
        """
        result = self.__dict__.copy()
        if result.get("created_at_iso"):
            result["created_at_iso"] = result["created_at_iso"].isoformat()
        return result

    def __str__(self):
        return str(self.to_dict())