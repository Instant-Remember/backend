from sqlalchemy.orm import Session
from sqlalchemy import and_

from models.likes import Like
from models.posts import Post
from schemas.posts import LikeBaseSchema, LikeSchema


def set_like(session: Session, like: LikeSchema) -> LikeSchema:
    db_like = Like(**like.dict())
    session.add(db_like)
    session.commit()
    session.refresh(db_like)

    return db_like


def unlike(session: Session, like) -> None:
    session.delete(like)
    session.commit()


def check(session: Session, user_id, post_id):
    like = session.query(Like).filter(and_(Like.user_id == user_id, Like.post_id == post_id)).one()
    return like


def get_likes(session: Session, post_id: int):
    post = session.query(Post).filter(Post.id == post_id).first()
    return post.likes
