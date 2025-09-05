import random
from datetime import timedelta, datetime, timezone
from typing import Any

import jwt
from app.core.config import get_settings


SECRET_KEY = get_settings().SECRET_KEY
ALGORITHM = get_settings().ALGORITHM
access_token_expire = get_settings().ACCESS_TOKEN_EXPIRE_MINUTES
refresh_token_expire = get_settings().REFRESH_TOKEN_EXPIRE_DAYS


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=access_token_expire)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    expires = timedelta(days=refresh_token_expire)
    return create_access_token(data, expires_delta=expires)


def generate_verification_code() -> str:
    return str(random.randint(100000, 999999))


def decode_jwt(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.InvalidTokenError:
        return None