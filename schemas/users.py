from pydantic import BaseModel, Field, EmailStr
from typing import Union

from datetime import datetime


class UserBaseSchema(BaseModel):
    username: str
    email: EmailStr
    first_name: str
    last_name: str
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
    email: Union[EmailStr, None]
    full_name: Union[str, None]
