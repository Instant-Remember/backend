from sqlalchemy.orm import Session

from models.goals import Goal
from models.posts import Post
from schemas.posts import PostBaseSchema, PostSchema


def create_post(session: Session, post: dict) -> PostSchema:
    db_post = Post(**post)
    session.add(db_post)
    session.commit()
    session.refresh(db_post)

    return db_post


def get_post_by_id(session: Session, id: int) -> PostSchema:

    return session.query(Post).filter(Post.id == id).one()


def get_post_owner(session: Session, post_id: int) -> int:
    db_post = session.query(Post).filter(Post.id == post_id).one()
    db_goal = session.query(Goal).filter(Goal.id == db_post.goal_id).one()

    return db_goal.owner_id


def patch_post(session: Session, post: Post) -> None:
    session.add(post)
    session.commit()


def delete_post(session: Session, post_id: int) -> None:
    db_post = session.query(Post).filter(Post.id == post_id).one()
    session.delete(db_post)
    session.commit()


def get_all_user_posts(session: Session, user_id):
    user_goals = session.query(Goal).filter(Goal.owner_id == user_id).all()
    posts = []
    for i in user_goals:
        posts += i.goal_posts

    return posts
