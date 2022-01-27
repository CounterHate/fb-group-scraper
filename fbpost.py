from dataclasses import dataclass, field, asdict


@dataclass
class Post:
    # form: str
    # original: bool
    post_id: int
    content: str
    date: str
    group_name: str
    group_id: int
    post_url: str
    author_id: int
    author_profile_url: str
    urls: list = field(default_factory=list)
    fanpage: bool = False
    like_count: int = 0
    comment_count: int = 0
    share_count: int = 0

    def to_dict(self):
        return asdict(self)


if __name__ == "__main__":
    import json

    post = Post(
        content="content",
        date="date",
        group=123456,
        post_url="post_url",
        urls=["link1", "link2"],
        author_id="author_id",
        author_profile_url="author_profile_url",
    )

    posts = [post.to_dict(), post.to_dict()]
    print(json.dumps(posts, indent=2))
