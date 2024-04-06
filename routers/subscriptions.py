from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

import datetime as dt

from config.db_initializer import get_db
from schemas.users import SubscribeSchema
from services.db import users as user_db_services
from services.db import subscriptions as subscription_db_services
from services.security.token import decode_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
router = APIRouter()


@router.get("/profile/{id}/follow")
def follow(
    id: int, token: str = Depends(oauth2_scheme), session: Session = Depends(get_db)
) -> dict:
    user_id = decode_token(token)["id"]

    try:
        user_db_services.get_user_by_id(session, id)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )

    try:
        sub_link = subscription_db_services.check(session, user_id, id)
    except NoResultFound:
        sub = SubscribeSchema(
            follower_id=user_id, publisher_id=id, date_create=dt.datetime.now(dt.UTC)
        )

        subscription_db_services.follow(session, sub)

        return {"status": "ok", "message": "Followed"}

    subscription_db_services.unfollow(session, sub_link)

    return {"status": "ok", "message": "Unfollowed"}


@router.get("/me/subscribers")
def get_current_user_subscribers(
    token: str = Depends(oauth2_scheme), session: Session = Depends(get_db)
):
    user_id = decode_token(token)["id"]

    subscribers = subscription_db_services.get_subscribers(
        session=session, user_id=user_id
    )

    return subscribers


@router.get("/me/subscriptions")
def get_current_user_subscriptions(
    token: str = Depends(oauth2_scheme), session: Session = Depends(get_db)
):
    user_id = decode_token(token)["id"]

    subscriptions = subscription_db_services.get_subscriptions(
        session=session, user_id=user_id
    )

    return subscriptions


@router.get("/profile/{id}/subscribers")
def get_profile_subscribers(id: int, session: Session = Depends(get_db)):
    try:
        user_db_services.get_user_by_id(session, id)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )

    return subscription_db_services.get_subscribers(session, id)


@router.get("/profile/{id}/subscriptions")
def get_profile_subscriptions(id: int, session: Session = Depends(get_db)):
    try:
        user_db_services.get_user_by_id(session, id)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )

    return subscription_db_services.get_subscriptions(session, id)
