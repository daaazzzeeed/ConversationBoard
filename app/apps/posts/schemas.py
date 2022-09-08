from pydantic import BaseModel
from typing import List, Optional


class PostCreate(BaseModel):
    text: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class PostComment(BaseModel):
    id: int


class PostShow(PostCreate):
    id: int
    comments: Optional[List[PostComment]] = None
    created_by: str
