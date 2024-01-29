from pydantic import BaseModel, EmailStr
from typing import Union

from datetime import datetime


class GoalBaseSchema(BaseModel):
    name: str
    description: str
    owner_id: int
    date_create: datetime
    date_modify: datetime


class GoalSchema(GoalBaseSchema):
    id: int
    class Config:
        orm_mode = True


class GoalUpdateSchema(BaseModel):
    email: Union[EmailStr, None]
    full_name: Union[str, None]
