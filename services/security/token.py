import jwt
from jwt.exceptions import DecodeError
import datetime as dt

from fastapi import APIRouter, Depends, HTTPException, status
from config.settings import SECRET_KEY


def decode_token(token: str) -> dict:
    # return jwt.decode(token, SECRET_KEY, algorithms="HS256")
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms="HS256")
        return decoded
    except DecodeError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token.")


def set_expiration(min: int):
    return dt.datetime.now(dt.UTC) + dt.timedelta(minutes=min)


def check_expiration(date):
    return dt.datetime.now(dt.UTC) < dt.datetime.fromtimestamp(date, dt.UTC)
