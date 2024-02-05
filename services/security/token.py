import jwt

from config.settings import SECRET_KEY


def decode_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms="HS256")
