from pydantic import BaseModel
from typing import Optional, List
from app.apps.posts.schemas import PostShow


class CommentCreate(BaseModel):
    text: str
    related_post_id: Optional[int] = None
    responds_to_comment_id: Optional[int] = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class ChildCommentShow(BaseModel):
    id: int
    text: str
    created_by: str


class CommentShow(CommentCreate):
    id: int
    related_post: Optional[PostShow] = None
    responds_to_comment_id: Optional[int] = None
    children_comments: Optional[List[ChildCommentShow]] = None
    created_by: str
