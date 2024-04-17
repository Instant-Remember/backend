from sqlalchemy.orm import Session
from sqlalchemy import or_, func

from models.users import User
from schemas.users import CreateUserSchema, UserSchema


def create_user(session: Session, user: dict) -> UserSchema:
    db_user = User(**user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


def get_user(session: Session, email: str) -> UserSchema:

    return session.query(User).filter(User.email == email).one()


def get_user_by_id(session: Session, id: int) -> UserSchema:

    return session.query(User).filter(User.id == id).one()


def get_goals(session: Session, user_id: int):
    user = session.query(User).filter(User.id == user_id).first()
    return user.user_goals


def edit_user(session: Session, user) -> UserSchema:
    session.add(user)
    session.commit()

    return user


def delete_user(session: Session, id: int) -> None:
    db_user = session.query(User).filter(User.id == id).one()
    session.delete(db_user)
    session.commit()


def search_users(session: Session, query: str):
    return (
        session.query(User)
        .filter(func.concat(User.first_name, " ", User.last_name).icontains(query))
        .all()
    )
