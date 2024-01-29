from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    SmallInteger,
    PrimaryKeyConstraint
)
from sqlalchemy.orm import relationship

from config.db_initializer import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, nullable=False, primary_key=True)
    text = Column(String, nullable=False)
    progress = Column(SmallInteger, default=0)
    goal_id = Column(Integer, ForeignKey('goals.id'))
    goal = relationship('Goal')
    date_create = Column(DateTime, nullable=False)
    date_modify = Column(DateTime, nullable=False)

    PrimaryKeyConstraint("id", name="pk_post_id")

    def __repr__(self):
        return "<Post - {id!r} from Goal {goal_id!r}>".format(id=self.id, goal_id=self.goal_id)
