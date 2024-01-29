import jwt


def decode_token(token: str) -> str:
    return jwt.decode(token, "ApplicationSecretKey", algorithms="HS256")
