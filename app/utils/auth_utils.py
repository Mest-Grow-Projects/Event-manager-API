import random
from datetime import timedelta, datetime, timezone
from typing import Dict
import jwt
from app.schemas.auth_schema import AuthToken, UserResponse
from decouple import config

JWT_SECRET = config("JWT_SECRET")
JWT_ALGORITHM = config("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_DAYS = 7


def generate_verification_code() -> str:
    return str(random.randint(100000, 999999))


def sign_jwt(payload: dict) -> str:
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token


def decode_jwt(token: str) -> dict | None:
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])


def create_login_tokens(user_data: UserResponse) -> Dict[str, str]:
    access_token_expires = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    access_payload = user_data.model_dump()
    access_payload["id"] = str(access_payload["id"])
    access_payload.update({
        "exp": access_token_expires,
        "token_type": AuthToken.ACCESS.value
    })
    access_token = sign_jwt(access_payload)

    refresh_payload = {
        "sub": str(user_data.id),
        "exp": refresh_token_expires,
        "token_type": AuthToken.REFRESH_TOKEN.value
    }
    refresh_token = sign_jwt(refresh_payload)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }