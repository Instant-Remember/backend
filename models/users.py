from sqlalchemy import (
    SmallInteger,
    LargeBinary,
    Column,
    String,
    Integer,
    Boolean,
    UniqueConstraint,
    DateTime,
)
from sqlalchemy.orm import relationship

from services.security.token import set_expiration
from config.db_initializer import Base
from config.settings import SECRET_KEY

import jwt
import bcrypt


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, nullable=False, primary_key=True)
    username = Column(String(40), nullable=False, unique=True)
    hashed_password = Column(LargeBinary, nullable=False)
    email = Column(String(225), nullable=False, unique=True)
    first_name = Column(String(15), nullable=False)
    last_name = Column(String(25), nullable=False)
    about = Column(String(50), nullable=True)
    status = Column(SmallInteger, nullable=True)
    profile_photo = Column(String, nullable=True)
    user_goals = relationship("Goal", back_populates="owner")
    user_comments = relationship("Comment", back_populates="user")
    user_likes = relationship("Like", back_populates="user")
    role = Column(String(15), nullable=False, default="USER")
    is_active = Column(Boolean, default=False)
    date_create = Column(DateTime, nullable=False)
    date_modify = Column(DateTime, nullable=False)

    UniqueConstraint("email", name="uq_user_email")
    UniqueConstraint("username", name="uq_user_username")

    @staticmethod
    def hash_password(password: str) -> bytes:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    def validate_password(self, password) -> bool:
        return self.hashed_password == bcrypt.hashpw(
            password.encode(), self.hashed_password
        )

    def generate_token(self) -> dict:
        return {
            "access_token": jwt.encode(
                {"id": self.id}, algorithm="HS256", key=SECRET_KEY
            )
        }

    def generate_reset_token(self) -> dict:
        return {
            "reset_token": jwt.encode(
                {"id": self.id, "exp": set_expiration(30)},
                algorithm="HS256",
                key=SECRET_KEY,
            )
        }
