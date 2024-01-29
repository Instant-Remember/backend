from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from config.db_initializer import get_db
from schemas.users import UserSchema, UserUpdateSchema
from services.db import users as user_db_services
from services.security.token import decode_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
router = APIRouter()


@router.get("/profile/{id}", response_model=UserSchema)
def profile(
        id: int,
        token: str = Depends(oauth2_scheme),
        session: Session = Depends(get_db)
):
    return user_db_services.get_user_by_id(session=session, id=id)


@router.get("/me", response_model=UserSchema)
def get_current_user(
        token: str = Depends(oauth2_scheme),
        session: Session = Depends(get_db)
):
    user_id = decode_token(token)

    return user_db_services.get_user_by_id(session=session, id=user_id['id'])


@router.put("/me")
def edit_current_user(
        data: UserUpdateSchema,
        token: str = Depends(oauth2_scheme),
        session: Session = Depends(get_db)
) -> dict:
    return data.dict(skip_defaults=True)