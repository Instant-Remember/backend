from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

import datetime as dt

from config.db_initializer import get_db
from schemas.posts import LikeSchema
from services.db import posts as post_db_services
from services.db import likes as like_db_services
from services.security.token import decode_token


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@router.get("/post/{id}/like")
def like_post(
    id: int, token: str = Depends(oauth2_scheme), session: Session = Depends(get_db)
) -> dict:
    try:
        user_id = decode_token(token)["id"]
        post_db_services.get_post_by_id(session, id)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found."
        )

    try:
        like = like_db_services.check(session, user_id, id)
    except NoResultFound:
        like = LikeSchema(
            user_id=user_id, post_id=id, date_create=dt.datetime.now(dt.UTC)
        )

        like_db_services.set_like(session, like)

        return {"status": "ok", "message": "Like set."}

    like_db_services.unlike(session, like)

    return {"status": "ok", "message": "Like unset."}


@router.get("/post/{id}/likes")
def get_post_likes(id: int, session: Session = Depends(get_db)):
    try:
        likes = like_db_services.get_likes(session, id)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found."
        )

    return likes
