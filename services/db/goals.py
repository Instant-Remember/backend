from sqlalchemy.orm import Session

from models.goals import Goal
from schemas.goals import GoalBaseSchema, GoalSchema


def create_goal(session: Session, goal: GoalBaseSchema) -> GoalSchema:
    db_goal = Goal(**goal.dict())
    session.add(db_goal)
    session.commit()
    session.refresh(db_goal)

    return db_goal


def get_goal_by_id(session: Session, id: int) -> GoalSchema:

    return session.query(Goal).filter(Goal.id == id).one()


def edit_goal(session: Session, goal: Goal) -> None:
    session.add(goal)
    session.commit()


def delete_goal(session: Session, id: int) -> None:
    db_goal = session.query(Goal).filter(Goal.id == id).one()
    session.delete(db_goal)
    session.commit()
