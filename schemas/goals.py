from pydantic import BaseModel
from typing import Union

from datetime import datetime


class GoalBaseSchema(BaseModel):
    name: str
    description: str


class GoalSchema(GoalBaseSchema):
    id: int
    owner_id: int
    date_create: datetime
    date_modify: datetime

    class Config:
        orm_mode = True


class GoalUpdateSchema(BaseModel):
    name: Union[str, None]
    description: Union[str, None]
