from typing import Annotated
from fastapi import Depends, HTTPException, status
from ..config import get_settings
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import InvalidTokenError
from ..constants import status_messages
from app.database.models.user import User, AccountStatus
from app.database.repository.user_repo import find_user_by_id
from app.schemas.auth_schema import TokenData


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
settings = get_settings()


async def get_authenticated_user(self, token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=status_messages["credentials_error"],
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception
        token_data = TokenData(sub=user_id)
    except InvalidTokenError:
        raise credentials_exception

    user = await find_user_by_id(token_data.sub)
    if user is None or user.accountStatus != AccountStatus.VERIFIED:
        raise credentials_exception

    return user