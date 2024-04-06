from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound


from config.db_initializer import get_db
from schemas.users import UserSchema, UserUpdateSchema
from services.db import users as user_db_services
from services.db import posts as post_db_services
from services.security.token import decode_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
router = APIRouter()


@router.get("/profile/{id}")
def get_profile(id: int, session: Session = Depends(get_db)) -> UserSchema:
    try:
        user = user_db_services.get_user_by_id(session=session, id=id)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )

    return user


@router.get("/me")
def get_current_user(
    token: str = Depends(oauth2_scheme), session: Session = Depends(get_db)
) -> UserSchema:

    user_id = decode_token(token)

    return user_db_services.get_user_by_id(session=session, id=user_id["id"])


@router.patch("/me")
def patch_current_user(
    payload: UserUpdateSchema,
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_db),
) -> dict:

    user = user_db_services.get_user_by_id(
        session=session, id=decode_token(token)["id"]
    )

    for name, value in payload.model_dump().items():
        setattr(user, name, value)

    user_db_services.edit_user(session=session, user=user)

    return {"status": "ok", "message": "User was updated"}


@router.delete("/me")
def delete_current_user(
    token: str = Depends(oauth2_scheme), session: Session = Depends(get_db)
) -> dict:

    user = decode_token(token)["id"]

    user_db_services.delete_user(session, user)

    return {"status": "ok", "message": "User was deleted"}


@router.get("/me/goals")
def get_current_user_goals(
    token: str = Depends(oauth2_scheme), session: Session = Depends(get_db)
):

    user_id = decode_token(token)["id"]

    return user_db_services.get_goals(session=session, user_id=user_id)


@router.get("/me/posts")
def get_current_user_posts(
    token: str = Depends(oauth2_scheme), session: Session = Depends(get_db)
):

    user_id = decode_token(token)["id"]

    return post_db_services.get_all_user_posts(session=session, user_id=user_id)


@router.get("/profile/{id}/goals")
def get_user_goals(user_id: int, session: Session = Depends(get_db)):
    try:
        goals = user_db_services.get_goals(session=session, user_id=user_id)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )

    return goals


@router.get("/profile/{id}/posts")
def get_user_posts(id: int, session: Session = Depends(get_db)):
    try:
        user_db_services.get_user_by_id(session, id)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )

    return post_db_services.get_all_user_posts(session=session, user_id=id)
