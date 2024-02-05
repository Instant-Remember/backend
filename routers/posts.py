from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

import datetime as dt

from config.db_initializer import get_db
from schemas.posts import PostSchema, PostBaseSchema, PostUpdateSchema, LikeSchema, LikeBaseSchema
from models.posts import Post
from services.db import posts as post_db_services
from services.db import goals as goal_db_services
from services.db import likes as like_db_services
from services.security.token import decode_token


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@router.post('/create')
def create_post(
    payload: PostBaseSchema = Body(),
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_db)
) -> PostSchema:

    try:
        goal = goal_db_services.get_goal_by_id(session, payload.goal_id)

    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found."
        )

    if decode_token(token)['id'] != goal.owner_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden"
        )

    return post_db_services.create_post(session, post=payload)


@router.get("/{id}")
def get_post_by_id(
        id: int,
        session: Session = Depends(get_db)
) -> Post:

    try:
        post: Post = post_db_services.get_post_by_id(
            session=session, id=id
        )

    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found."
        )

    return post


@router.patch("/{id}")
def patch_post(
    id: int,
    payload: PostUpdateSchema,
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_db)
) -> dict:

    try:
        post_db = post_db_services.get_post_by_id(session=session, id=id)

    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found."
        )

    if post_db_services.get_post_owner(session=session, post_id=id) != decode_token(token)["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden"
        )

    for name, value in payload.model_dump().items():
        setattr(post_db, name, value)

    post_db.date_modify = dt.datetime.now(dt.UTC)

    post_db_services.patch_post(session=session, post=post_db)

    return {"message": "ok"}


@router.delete("/{id}")
def delete_post(
        id: int,
        token: str = Depends(oauth2_scheme),
        session: Session = Depends(get_db)
) -> dict:

    post_owner = post_db_services.get_post_owner(session, id)

    if post_owner == decode_token(token)['id']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden"
        )

    post_db_services.delete_post(session=session, post_id=id)

    return {"message": "ok"}


@router.get("/{id}/like")
def like_post(
        id: int,
        token: str = Depends(oauth2_scheme),
        session: Session = Depends(get_db)
) -> dict:

    try:
        post_db_services.get_post_by_id(session, id)

    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found."
        )

    user_id = decode_token(token)['id']

    like = LikeSchema(
        user_id=user_id,
        post_id=id,
        date_create=dt.datetime.now(dt.UTC)
    )

    like_db_services.set_like(session, like)

    return {'message': 'ok'}


@router.delete("/{id}/unlike")
def unlike_post(
    id: int,
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_db)
) -> dict:

    like = LikeBaseSchema(
        user_id=decode_token(token)['id'],
        post_id=id
    )

    like_db_services.unlike(session, like)

    return {'message': 'ok'}
