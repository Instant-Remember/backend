from pydantic import BaseModel, Field, EmailStr
from typing import Union

from datetime import datetime


class UserBaseSchema(BaseModel):
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    about: Union[str, None]
    status: Union[int, None]
    role: str
    date_create: datetime
    date_modify: datetime


class CreateUserSchema(UserBaseSchema):
    hashed_password: str = Field(alias="password")


class UserSchema(UserBaseSchema):
    id: int
    is_active: bool = Field(default=False)

    class Config:
        orm_mode = True


class UserLoginSchema(BaseModel):
    email: EmailStr = Field(alias="username")
    password: str


class UserUpdateSchema(BaseModel):
    username: Union[str, None]
    first_name: Union[str, None]
    last_name: Union[str, None]
    about: Union[str, None]
    status: Union[int, None]

class SubscribeBaseSchema(BaseModel):
    publisher_id: int
    follower_id: int

class SubscribeSchema(SubscribeBaseSchema):
    date_create: datetime


