from sqlalchemy.orm import Session

from models.comments import Comment
from schemas.posts import CommentBaseSchema, CommentSchema


def create_comment(session: Session, goal: CommentBaseSchema) -> CommentSchema:
    db_comment = Comment(**goal.dict())
    session.add(db_comment)
    session.commit()
    session.refresh(db_comment)

    return db_comment


def get_comment_by_id(session: Session, id: int) -> CommentSchema:

    return session.query(Comment).filter(Comment.id == id).one()


def edit_comment(session: Session, comment: Comment) -> None:
    session.add(comment)
    session.commit()


def delete_comment(session: Session, id: int) -> None:
    db_comment = session.query(Comment).filter(Comment.id == id).one()
    session.delete(db_comment)
    session.commit()
