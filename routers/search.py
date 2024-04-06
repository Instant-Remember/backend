from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from config.db_initializer import get_db
from services.db import users as user_db_services
from services.db import goals as goal_db_services


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
router = APIRouter()


@router.get("/users/{query}")
def search_users(query: str, session: Session = Depends(get_db)):
    return user_db_services.search_users(session, query)


@router.get("/goals/{query}")
def search_goals(query: str, session: Session = Depends(get_db)):
    return goal_db_services.search_goals(session, query)
