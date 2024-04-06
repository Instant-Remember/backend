from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from config.db_initializer import Base


class Like(Base):
    __tablename__ = "likes"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    user = relationship("User", back_populates="user_likes")
    post_id = Column(Integer, ForeignKey("posts.id"), primary_key=True)
    post = relationship("Post", back_populates="likes")
    date_create = Column(DateTime, nullable=False)
