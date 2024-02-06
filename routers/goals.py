from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

import datetime as dt

from config.db_initializer import get_db
from schemas.goals import GoalSchema, GoalBaseSchema, GoalUpdateSchema
from models.goals import Goal
from services.db import goals as goal_db_services
from services.security.token import decode_token


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@router.post('/create')
def create_goal(
    payload: GoalBaseSchema = Body(),
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_db)
) -> GoalSchema:

    if decode_token(token)['id'] != payload.owner_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden"
        )

    return goal_db_services.create_goal(session, goal=payload)


@router.get("/{id}")
def get_goal_by_id(
        id: int,
        session: Session = Depends(get_db)
) -> GoalSchema:

    try:
        goal: Goal = goal_db_services.get_goal_by_id(
            session=session, id=id
        )

    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found."
        )

    return goal


@router.patch("/{id}")
def patch_goal(
    id: int,
    payload: GoalUpdateSchema,
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_db)
) -> dict:

    try:
        goal_db = goal_db_services.get_goal_by_id(session=session, id=id)

    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found."
        )

    if goal_db.owner_id != decode_token(token)["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden"
        )

    for name, value in payload.model_dump().items():
        setattr(goal_db, name, value)

    goal_db.date_modify = dt.datetime.now(dt.UTC)

    goal_db_services.edit_goal(session=session, goal=goal_db)

    return {"message": "ok"}


@router.delete("/{id}")
def delete_goal(
    id: int,
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_db)
) -> dict:

    goal = goal_db_services.get_goal_by_id(session, id)

    if goal.owner_id != decode_token(token)["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden"
        )

    goal_db_services.delete_goal(session, id)

    return {"message": "Deleted"}
