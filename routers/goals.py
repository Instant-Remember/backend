from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from config.db_initializer import get_db
from models import goals as goal_model
from services.db import goals as goal_db_services
from schemas.goals import GoalSchema, GoalBaseSchema
from services.security.token import decode_token


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@router.post('/create', response_model=GoalSchema)
def create_goal(
    payload: GoalBaseSchema = Body(),
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_db)
):
    if decode_token(token)['id'] == payload.owner_id:
        return goal_db_services.create_goal(session, goal=payload)
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
        goal: goal_model.Goal = goal_db_services.get_goal_by_id(
            session=session, id=id
        )
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found."
        )

    return goal
