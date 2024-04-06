from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from config.db_initializer import Base


class Goal(Base):
    __tablename__ = "goals"

    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(250), nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="user_goals")
    goal_posts = relationship("Post", back_populates="goal")
    date_create = Column(DateTime, nullable=False)
    date_modify = Column(DateTime, nullable=False)
