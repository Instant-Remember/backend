from sqlalchemy.orm import Session

from models.goals import Goal
from schemas.goals import GoalBaseSchema


def create_goal(session: Session, goal: GoalBaseSchema):
    db_goal = Goal(**goal.dict())
    session.add(db_goal)
    session.commit()
    session.refresh(db_goal)
    return db_goal


def get_goal_by_id(session: Session, id: int):
    return session.query(Goal).filter(Goal.id == id).one()
