from sqlalchemy.orm import Session

from models.subscriptions import Subscription
from schemas.users import SubscribeBaseSchema, SubscribeSchema


def follow(session: Session, subscription: SubscribeSchema) -> SubscribeSchema:
    db_subscription = Subscription(**subscription.dict())
    session.add(db_subscription)
    session.commit()
    session.refresh(db_subscription)

    return db_subscription


def unfollow(session: Session, db_sub) -> None:
    session.delete(db_sub)
    session.commit()

def check(session: Session, user_id, author_id):
    db_sub = (
        session.query(Subscription)
        .filter(
            Subscription.publisher_id == author_id,
            Subscription.follower_id == user_id,
        )
        .one()
    )

    return db_sub


def get_subscribers(session: Session, user_id):
    return (
        session.query(Subscription).filter(Subscription.publisher_id == user_id).all()
    )


def get_subscriptions(session: Session, user_id):
    return session.query(Subscription).filter(Subscription.follower_id == user_id).all()
