from pydantic import BaseModel
from typing import Union

from datetime import datetime


class PostBaseSchema(BaseModel):
    text: str
    progress: int
    goal_id: int
    date_create: datetime
    date_modify: datetime


class PostSchema(PostBaseSchema):
    id: int
    class Config:
        orm_mode = True

class PostUpdateSchema(BaseModel):
    text: Union[str, None]
    progress: Union[int, None]

class LikeBaseSchema(BaseModel):
    user_id: int
    post_id: int

class LikeSchema(LikeBaseSchema):
    date_create: datetime
