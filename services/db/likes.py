from sqlalchemy.orm import Session

from models.likes import Like
from schemas.posts import LikeBaseSchema, LikeSchema


def set_like(session: Session, like: LikeSchema) -> LikeSchema:
    db_like = Like(**like.dict())
    session.add(db_like)
    session.commit()
    session.refresh(db_like)

    return db_like


def unlike(session: Session, like: LikeBaseSchema) -> None:
    db_like = session.query(Like).filter(
        Like.user_id == like.user_id,
        Like.post_id == like.post_id
    ).one()
    session.delete(db_like)
    session.commit()
