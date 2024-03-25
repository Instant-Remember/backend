import jwt
import datetime as dt

from config.settings import SECRET_KEY


def decode_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms="HS256")

def set_expiration(min: int):
    return dt.datetime.now(dt.UTC) + dt.timedelta(minutes=min)

def check_expiration(date):
    return dt.datetime.now(dt.UTC) < dt.datetime.fromtimestamp(date, dt.UTC)