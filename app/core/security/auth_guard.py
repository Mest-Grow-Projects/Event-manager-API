from typing import Annotated
from fastapi import Header, HTTPException, status
from ..config import get_settings
from ..constants import status_messages
from app.database.repository.user_repo import find_user_by_id
from app.schemas.auth_schema import UserResponse
from app.utils.auth_utils import decode_jwt

settings = get_settings()
AUTH_PREFIX = 'Bearer'


async def get_authenticated_user(authorization: Annotated[str | None, Header()] = None) -> UserResponse:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=status_messages["credentials_error"],
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not authorization:
        raise credentials_exception
    if not authorization.startswith(AUTH_PREFIX):
        raise credentials_exception

    payload = decode_jwt(token=authorization[len(AUTH_PREFIX):])
    if payload and payload["sub"]:
        try:
            user = await find_user_by_id(payload['sub'])
            return UserResponse(
                id = str(user.id),
                name = user.name,
                email = str(user.email),
                role = user.role,
                accountStatus = user.accountStatus
            )
        except Exception as error:
            raise error
    raise credentials_exception