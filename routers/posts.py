from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

import datetime as dt

from config.db_initializer import get_db
from schemas.posts import PostSchema, PostBaseSchema, PostUpdateSchema
from services.db import posts as post_db_services
from services.db import goals as goal_db_services
from services.db import comments as comment_db_services
from services.security.token import decode_token


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@router.post("/")
def create_post(
    payload: PostBaseSchema = Body(),
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_db),
) -> PostSchema:
    try:
        goal = goal_db_services.get_goal_by_id(session, payload.goal_id)

    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found."
        )

    if decode_token(token)["id"] != goal.owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    post = payload.dict()
    now = dt.datetime.now(dt.UTC)
    post['owner_id'] = goal.owner_id
    post['date_create'] = now
    post['date_modify'] = now

    return post_db_services.create_post(session, post=post)


@router.get("/{id}")
def get_post(id: int, session: Session = Depends(get_db)) -> PostSchema:
    try:
        post: PostSchema = post_db_services.get_post_by_id(session=session, id=id)
        post.likes_count = len(post.likes)

    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found."
        )

    return post


@router.patch("/{id}")
def patch_post(
    id: int,
    payload: PostUpdateSchema,
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_db),
) -> dict:
    try:
        post_db = post_db_services.get_post_by_id(session=session, id=id)

    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found."
        )

    if (
        post_db_services.get_post_owner(session=session, post_id=id)
        != decode_token(token)["id"]
    ):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    for name, value in payload.model_dump().items():
        setattr(post_db, name, value)

    post_db.date_modify = dt.datetime.now(dt.UTC)

    post_db_services.patch_post(session=session, post=post_db)

    return {"status": "ok", "message": "Post was edited."}


@router.delete("/{id}")
def delete_post(
    id: int, token: str = Depends(oauth2_scheme), session: Session = Depends(get_db)
) -> dict:
    post_owner = post_db_services.get_post_owner(session, id)

    if post_owner != decode_token(token)["id"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    post_db_services.delete_post(session=session, post_id=id)

    return {"status": "ok", "message": "Post was deleted."}


@router.get("/{id}/comments")
def get_post_comments(id: int, session: Session = Depends(get_db)):
    try:
        comments = comment_db_services.get_comments_by_post_id(session, id)

    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found."
        )

    return comments
