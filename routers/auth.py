from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from config.db_initializer import get_db
from schemas.users import (
    CreateUserSchema,
    UserSchema,
    ResetUserPasswordSchema,
    ChangePasswordSchema,
)
from models.users import User
from services.db import users as user_db_services
from services.mailer.mailer import Mailer
from services.security.password_generator import generate
from services.security.token import decode_token

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@router.post("/signup")
def signup(
    payload: CreateUserSchema = Body(), session: Session = Depends(get_db)
) -> UserSchema:

    payload.hashed_password = User.hash_password(payload.hashed_password)
    payload.email = payload.email.lower()

    return user_db_services.create_user(session, user=payload)


@router.post("/login")
def login(
    payload: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_db)
) -> dict:

    try:
        user: UserSchema = user_db_services.get_user(
            session=session, email=payload.username.lower()
        )

    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user credentials"
        )

    is_validated: bool = user.validate_password(payload.password)
    if not is_validated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password"
        )

    return user.generate_token()


@router.post("/reset")
def reset_password(
    payload: ResetUserPasswordSchema,
    session: Session = Depends(get_db),
):

    try:
        user = user_db_services.get_user(session, payload.email)
    except:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Invalid email"
        )

    new_password = generate()
    Mailer.send_email(payload.email, new_password)
    user.hashed_password = User.hash_password(new_password)
    user_db_services.edit_user(session, user)

    return {"status": "ok", "message": "New password sent to your email."}


@router.post("/change_password")
def change_password(
    payload: ChangePasswordSchema,
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_db),
):

    user = decode_token(token)["id"]

    if payload.new_password == payload.re_password:
        user.hashed_password = User.hash_password(payload.new_password)
        user_db_services.edit_user(session, user)

        return {"status": "ok", "message": "Password changed."}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords don't match."
        )
