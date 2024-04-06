from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from config.db_initializer import Base


class Subscription(Base):
    __tablename__ = "subscriptions"

    publisher_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    publisher = relationship("User", foreign_keys=publisher_id)
    follower_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    follower = relationship("User", foreign_keys=follower_id)
    date_create = Column(DateTime, nullable=False)
