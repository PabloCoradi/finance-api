from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")


def hash_password(password: str) -> str:
    hashed_password = pwd_context.hash(password)

    return hashed_password


def verify_password(plain_password: str, hashed_password: str) -> bool:
    if pwd_context.verify(plain_password, hashed_password):
        return True

    return False


def create_access_token(data: dict) -> str:
    expiration_time = datetime.now(timezone.utc) + timedelta(hours=1)
    payload = {
        **data,
        "exp": int(expiration_time.timestamp())
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    return token