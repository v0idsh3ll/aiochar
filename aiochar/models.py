from datetime import datetime


class Post:
    def __init__(
        self,
        post_id: int,
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
        repost_text: str | None = None
    ) -> None:

        self.post_id = int(post_id)
        self.user_id = int(user_id)
        self.username = str(username)

        self.api_bot = bool(api_bot)
        self.flair = flair or []

        self.content = content or ""
        self.content_html = content_html or ""

        try:
            self.created_at_iso = datetime.fromisoformat(created_at_iso.replace("Z", "+00:00"))
        except Exception:
            self.created_at = None

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
        return {
            "post_id": self.post_id,
            "user_id": self.user_id,
            "username": self.username,
            "api_bot": self.api_bot,
            "flair": self.flair,
            "content": self.content,
            "content_html": self.content_html,
            "created_at_iso": self.created_at_iso.isoformat() if self.created_at_iso else None,
            "country_code": self.country_code,
            "like_post_id": self.like_post_id,
            "like_count": self.like_count,
            "reply_count": self.reply_count,
            "repost_count": self.repost_count,
            "is_liked": self.is_liked,
            "is_own_post": self.is_own_post,
            "hashtags": self.hashtags,
            "mentions": self.mentions,
            "repost_of_id": self.repost_of_id,
            "repost_text": self.repost_text
        }

    def __str__(self):
        return str(self.to_dict())