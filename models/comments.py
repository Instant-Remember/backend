from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey
)
from sqlalchemy.orm import relationship

from config.db_initializer import Base

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, nullable=False, primary_key=True)
    text = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User')
    post_id = Column(Integer, ForeignKey('posts.id'))
    post = relationship("Post")
    date_create = Column(DateTime, nullable=False)
    date_modify = Column(DateTime, nullable=False)