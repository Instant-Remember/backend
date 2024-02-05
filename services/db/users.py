from sqlalchemy.orm import Session

from models.users import User
from schemas.users import CreateUserSchema, UserSchema


def create_user(session: Session, user: CreateUserSchema) -> UserSchema:
    db_user = User(**user.dict())
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


def get_user(session: Session, email: str) -> UserSchema:

    return session.query(User).filter(User.email == email).one()


def get_user_by_id(session: Session, id: int) -> UserSchema:

    return session.query(User).filter(User.id == id).one()


def edit_user(session: Session, user) -> UserSchema:
    session.add(user)
    session.commit()

    return user


def delete_user(session: Session, id: int) -> None:
    db_user = session.query(User).filter(User.id == id).one()
    session.delete(db_user)
    session.commit()
