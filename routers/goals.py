from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

import datetime as dt

from config.db_initializer import get_db
from schemas.goals import GoalSchema, GoalBaseSchema, GoalUpdateSchema
from schemas.posts import PostSchema
from services.db import goals as goal_db_services
from services.security.token import decode_token


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@router.post("")
def create_goal(
    payload: GoalBaseSchema = Body(),
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_db),
) -> GoalSchema:

    goal = payload.dict()
    goal['owner_id'] = decode_token(token)["id"]
    now = dt.datetime.now(dt.UTC)
    goal['date_create'] = now
    goal['date_modify'] = now

    return goal_db_services.create_goal(session, goal=goal)


@router.get("/{id}")
def get_goal(id: int, session: Session = Depends(get_db)) -> GoalSchema:

    try:
        goal = goal_db_services.get_goal_by_id(session=session, id=id)

    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found."
        )

    return goal


@router.patch("/{id}")
def patch_goal(
    id: int,
    payload: GoalUpdateSchema,
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_db),
) -> dict:

    try:
        goal_db = goal_db_services.get_goal_by_id(session=session, id=id)

    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found."
        )

    if goal_db.owner_id != decode_token(token)["id"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    for name, value in payload.model_dump().items():
        setattr(goal_db, name, value)

    goal_db.date_modify = dt.datetime.now(dt.UTC)

    goal_db_services.edit_goal(session=session, goal=goal_db)

    return {"status": "ok", "message": "Goal was edit."}


@router.delete("/{id}")
def delete_goal(
    id: int, token: str = Depends(oauth2_scheme), session: Session = Depends(get_db)
) -> dict:

    goal = goal_db_services.get_goal_by_id(session, id)

    if goal.owner_id != decode_token(token)["id"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    goal_db_services.delete_goal(session, id)

    return {"status": "ok", "message": "Goal was deleted"}


@router.get("/{id}/posts")
def get_goal_posts(id: int, session: Session = Depends(get_db)) -> list[PostSchema]:

    try:
        posts: list[PostSchema] = goal_db_services.get_posts_by_goal_id(session=session, goal_id=id)
        for post in posts:
            post.likes_count = len(post.likes)
            del post.likes

    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found."
        )

    return posts
