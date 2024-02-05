from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

import datetime as dt

from config.db_initializer import get_db
from schemas.users import UserSchema, UserUpdateSchema, SubscribeSchema, SubscribeBaseSchema
from services.db import users as user_db_services
from services.db import subscriptions as subscription_db_services
from services.security.token import decode_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
router = APIRouter()


@router.get("/profile/{id}")
def profile(
        id: int,
        session: Session = Depends(get_db)
) -> UserSchema:

    return user_db_services.get_user_by_id(session=session, id=id)


@router.get("/me")
def get_current_user(
        token: str = Depends(oauth2_scheme),
        session: Session = Depends(get_db)
) -> UserSchema:

    user_id = decode_token(token)

    return user_db_services.get_user_by_id(session=session, id=user_id['id'])


@router.patch("/me")
def edit_current_user(
        payload: UserUpdateSchema,
        token: str = Depends(oauth2_scheme),
        session: Session = Depends(get_db)
) -> dict:

    user = user_db_services.get_user_by_id(session, decode_token(token)["id"])

    for name, value in payload.model_dump().items():
        setattr(user, name, value)

    user_db_services.edit_user(session, user)

    return {"message": "ok"}


@router.delete("/me")
def delete_current_user(
        token: str = Depends(oauth2_scheme),
        session: Session = Depends(get_db)
) -> dict:

    user = decode_token(token)["id"]

    user_db_services.delete_user(session, user)

    return {"message": "User deleted"}


@router.get("/{id}/follow")
def follow(
        id: int,
        token: str = Depends(oauth2_scheme),
        session: Session = Depends(get_db)
) -> dict:

    try:
        user_db_services.get_user_by_id(session, id)

    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found."
        )

    user_id = decode_token(token)['id']

    like = SubscribeSchema(
        follower_id=user_id,
        publisher_id=id,
        date_create=dt.datetime.now(dt.UTC)
    )

    subscription_db_services.follow(session, like)

    return {'message': 'Followed'}

@router.delete("/{id}/unfollow")
def unfollow(
        id: int,
        token: str = Depends(oauth2_scheme),
        session: Session = Depends(get_db)
) -> dict:

    sub = SubscribeBaseSchema(
        publisher_id=id,
        follower_id=decode_token(token)['id']
    )

    subscription_db_services.unfollow(session, sub)

    return {'message': 'Unfollowed'}
