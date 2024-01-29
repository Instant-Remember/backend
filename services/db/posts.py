from sqlalchemy.orm import Session

from models.posts import Post
from schemas.posts import PostBaseSchema


def create_post(session: Session, post: PostBaseSchema):
    db_post = Post(**post.dict())
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post


def get_post_by_id(session: Session, id: int):
    return session.query(Post).filter(Post.id == id).one()
