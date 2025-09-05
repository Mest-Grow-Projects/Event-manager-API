import random
from datetime import timedelta, datetime, timezone
from typing import Annotated
from fastapi import Depends, HTTPException, status
import jwt
from jwt.exceptions import InvalidTokenError
from app.core.config import get_settings
from fastapi.security import OAuth2PasswordBearer
from app.core.constants import status_messages
from app.database.models.user import User
from app.schemas.auth_schema import TokenData
from app.database.repository.user_repo import find_user_by_id

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=status_messages["credentials_error"],
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(sub=user_id)
    except InvalidTokenError:
        raise credentials_exception

    user = await find_user_by_id(token_data.sub)
    if user is None:
        raise credentials_exception
    return user


def generate_verification_code() -> str:
    return str(random.randint(100000, 999999))
