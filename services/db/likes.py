from sqlalchemy.orm import Session

from models.likes import Like
from schemas.posts import LikeSchema


def set_like(session: Session, like: LikeSchema):
    db_like = Like(**like.dict())
    session.add(db_like)
    session.commit()
    session.refresh(db_like)
    return db_like
