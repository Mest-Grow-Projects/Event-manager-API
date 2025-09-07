from fastapi import HTTPException, status
from pydantic import BaseModel
from app.core.security.password_hash import get_password_hash
from app.database.models.user import User, Roles, AccountStatus
from app.core.config.constants import status_messages
from app.schemas.auth_schema import SignupSchema


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
    role: Roles = Roles.ATTENDEE,
    account_status: AccountStatus = AccountStatus.PENDING
) -> User:
    await check_existing_user(str(user.email))
    hashed_password = get_password_hash(user.password)
    new_user = User(
        name=user.name,
        email=str(user.email),
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


async def get_and_validate_user(user_id: str) -> User:
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=status_messages["user_id_required"],
        )
    user = await find_user_by_id(user_id)
    return user


def validate_updated_data(data: BaseModel):
    updated_data = data.model_dump(exclude_unset=True, exclude_none=True)

    if not updated_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=status_messages["update_invalid"],
        )
    return updated_data