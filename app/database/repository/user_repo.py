from fastapi import HTTPException, status
from app.database.models.user import User, Roles, AccountStatus
from app.core.constants import status_messages
from app.schemas.auth_schema import SignupSchema
from app.utils.auth_utils import get_password_hash


async def find_user_by_email(email: str) -> User:
    user = await User.find_one(User.email == email.lower())
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=status_messages["not_found"]
        )
    return user


async def find_user_by_id(user_id: str) -> User:
    user = await User.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=status_messages["not_found"]
        )
    return user


async def check_existing_user(email: str) -> bool:
    existing_user = await User.find_one(User.email == email.lower())
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=status_messages["conflict"]
        )
    return False


async def create_user(
    user: SignupSchema,
    role: Roles,
    account_status: AccountStatus = AccountStatus.PENDING
) -> User:
    await check_existing_user(str(user.email))
    hashed_password = get_password_hash(user.password)
    new_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        role=role,
        accountStatus=account_status,
    )
    await new_user.insert()

    if not new_user:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=status_messages["failed_user"]
        )
    return new_user