from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, SmallInteger
from sqlalchemy.orm import relationship

from config.db_initializer import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, nullable=False, primary_key=True)
    text = Column(String, nullable=False)
    progress = Column(SmallInteger, default=0)
    owner_id = Column(Integer, nullable=False)
    goal_id = Column(Integer, ForeignKey("goals.id"))
    goal = relationship("Goal", back_populates="goal_posts")
    comments = relationship("Comment", back_populates="post")
    likes = relationship("Like", back_populates="post")
    date_create = Column(DateTime, nullable=False)
    date_modify = Column(DateTime, nullable=False)
