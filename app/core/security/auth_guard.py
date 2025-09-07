from typing import Annotated
from fastapi import Header, HTTPException, status
from app.core.constants import status_messages, validations, error_messages
from app.database.repository.user_repo import find_user_by_id
from app.schemas.auth_schema import UserResponse
from app.utils.auth_utils import decode_jwt
import jwt


AUTH_PREFIX = 'Bearer'


async def get_authenticated_user(authorization: Annotated[str | None, Header()] = None) -> UserResponse:
    if not authorization or not authorization.startswith(AUTH_PREFIX):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=status_messages["credentials_error"]
        )

    token = authorization[len(AUTH_PREFIX):].strip()

    try:
        payload = decode_jwt(token)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=error_messages["expired_token"]
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=validations["invalid_token"]
        )

    user_id = payload.get("sub") or payload.get("id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=validations["invalid_payload"]
        )

    try:
        user = await find_user_by_id(user_id)
        return UserResponse(
            id = user.id,
            name = user.name,
            email = user.email,
            role = user.role,
            accountStatus = user.accountStatus
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_messages["internal_error"]
        )