from pydantic import BaseModel

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


class LikeSchema(BaseModel):
    user_id: int
    post_id: int
    date_create: datetime
