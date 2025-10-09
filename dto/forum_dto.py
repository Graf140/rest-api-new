from dataclasses import dataclass


@dataclass
class CreatePostDTO:
    title: str
    content: str
    user_id: int


@dataclass
class GetForumPostDTO: #сомнительно
    post_id: int
