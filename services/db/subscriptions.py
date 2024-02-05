from sqlalchemy.orm import Session

from models.subscriptions import Subscription
from schemas.users import SubscribeBaseSchema, SubscribeSchema


def follow(session: Session, subscription: SubscribeSchema) -> SubscribeSchema:
    db_subscription = Subscription(**subscription.dict())
    session.add(db_subscription)
    session.commit()
    session.refresh(db_subscription)

    return db_subscription


def unfollow(session: Session, subscription: SubscribeBaseSchema) -> None:
    db_sub = session.query(Subscription).filter(
        Subscription.publisher_id == subscription.publisher_id,
        Subscription.follower_id == subscription.follower_id
    ).one()
    session.delete(db_sub)
    session.commit()
