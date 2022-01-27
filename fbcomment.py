from dataclasses import dataclass, field, asdict


@dataclass
class Comment:
    original_post_id: int
    comment_id: int
    content: str
    date: str
    group_id: int
    group_name: str
    author_id: int
    author_profile_url: str
    replies: list = field(default_factory=list)
    reaction_count: int = 0

    def to_dict(self):
        return asdict(self)


if __name__ == "__main__":
    pass
