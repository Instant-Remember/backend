import os
import secrets

DATABASE_URL = (
    "postgresql+psycopg2://{username}:{password}@{host}:{port}/{db_name}".format(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        db_name=os.getenv("POSTGRES_DB"),
        username=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )
)

SMTP = {
    "USER": os.getenv("SMTP_USER"),
    "PASS": os.getenv("SMTP_PASS"),
    "HOST": os.getenv("SMTP_HOST"),
    "PORT": os.getenv("SMTP_PORT"),
}

S3 = {
    "KEY_ID": os.getenv("S3_KEY_ID"),
    "SECRET_KEY": os.getenv("S3_SECRET_KEY"),
    "BUCKET_NAME": os.getenv("S3_BUCKET_NAME")
}


SECRET_KEY = secrets.token_hex(32)
