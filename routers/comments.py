from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

import datetime as dt

from config.db_initializer import get_db
from schemas.posts import (
    CommentBaseSchema,
    CommentSchema,
    CommentUpdateSchema,
)
from services.db import posts as post_db_services
from services.db import comments as comment_db_services
from services.security.token import decode_token


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@router.post("/comment/create")
def create_comment(
    payload: CommentBaseSchema = Body(),
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_db),
) -> CommentSchema:

    try:
        post = post_db_services.get_post_by_id(session, payload.post_id)

    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not exist."
        )

    if decode_token(token)["id"] != payload.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    return comment_db_services.create_comment(session, comment=payload)


@router.patch("/comment/{id}")
def patch_comment(
    id: int,
    payload: CommentUpdateSchema = Body(),
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_db),
) -> dict:

    try:
        comment_db = comment_db_services.get_comment_by_id(session, id)

    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment not exist."
        )

    if decode_token(token)["id"] != comment_db.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    for name, value in payload.model_dump().items():
        setattr(comment_db, name, value)

    comment_db.date_modify = dt.datetime.now(dt.UTC)

    comment_db_services.edit_comment(session=session, comment=comment_db)

    return {"status": "ok", "message": "Comment was edit"}


@router.get("/comment/{id}")
def get_comment(id: int, session: Session = Depends(get_db)):

    try:
        comment = comment_db_services.get_comment_by_id(session, id)

    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found.")

    return comment


@router.delete("/comment/{id}")
def delete_comment(
    id: int, token: str = Depends(oauth2_scheme), session: Session = Depends(get_db)
):

    try:
        comment = comment_db_services.get_comment_by_id(session, id)
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found.")

    if decode_token(token)["id"] != comment.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    comment_db_services.delete_comment(session, id)

    return {"status": "ok", "message": "Comment was deleted"}
