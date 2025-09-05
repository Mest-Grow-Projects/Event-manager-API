from typing import List, Annotated
from app.core.security.auth_guard import get_authenticated_user
from app.database.models.user import Roles, User
from fastapi import Depends, HTTPException, status


class RoleGuard:
    def __init__(self, allowed_roles: List[Roles]):
        self.allowed_roles = allowed_roles

    async def __call__(self, user: Annotated[User, Depends(get_authenticated_user)]) -> User:
        if user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User {user.role} is not allowed to access this resource",
            )

        return user