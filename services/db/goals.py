from sqlalchemy.orm import Session
from sqlalchemy import or_

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


def get_posts_by_goal_id(session: Session, goal_id: int) -> list[GoalSchema]:
    goal = session.query(Goal).filter(Goal.id == goal_id).first()
    return goal.goal_posts


def edit_goal(session: Session, goal: Goal) -> None:
    session.add(goal)
    session.commit()


def delete_goal(session: Session, id: int) -> None:
    db_goal = session.query(Goal).filter(Goal.id == id).one()
    session.delete(db_goal)
    session.commit()


def search_goals(session: Session, query: str):
    return (
        session.query(Goal)
        .filter(or_(Goal.name.icontains(query), Goal.description.icontains(query)))
        .all()
    )
