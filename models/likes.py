from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
    PrimaryKeyConstraint
)
from sqlalchemy.orm import relationship

from config.db_initializer import Base


class Like(Base):
    __tablename__ = "likes"

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    user = relationship("User")
    post_id = Column(Integer, ForeignKey('posts.id'), primary_key=True)
    post = relationship("Post")
    date_create = Column(DateTime, nullable=False)

    PrimaryKeyConstraint("user_id", name="pk_like_user_id")
    PrimaryKeyConstraint("post_id", name="pk_like_post_id")

    def __repr__(self):
        return "<Post - {id!r} from Goal {goal_id!r}>".format(id=self.id, goal_id=self.goal_id)
