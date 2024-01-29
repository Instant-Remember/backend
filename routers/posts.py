from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from config.db_initializer import get_db
from models import posts as post_model
from services.db import posts as post_db_services
from services.db import goals as goal_db_services
from services.db import likes as like_db_services
from schemas.posts import PostSchema, PostBaseSchema, LikeSchema
from services.security.token import decode_token

import datetime as dt


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@router.post('/create', response_model=PostSchema)
def create_post(
    payload: PostBaseSchema = Body(),
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_db)
):
    try:
        goal = goal_db_services.get_goal_by_id(session, payload.goal_id)

    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found."
        )

    if decode_token(token)['id'] == goal.owner_id:
        return post_db_services.create_post(session, post=payload)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden"
        )


@router.get("/{id}")
def get_goal_by_id(
        id: int,
        session: Session = Depends(get_db)
):
    try:
        goal: post_model.Post = post_db_services.get_post_by_id(
            session=session, id=id
        )
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found."
        )

    return goal

@router.get("/{id}/like")
def like_post(
        id: int,
        token: str = Depends(oauth2_scheme),
        session: Session = Depends(get_db)
):
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

    return {'message': 'Successful'}
