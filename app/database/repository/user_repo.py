from fastapi import HTTPException, status
from app.database.models.user import User
from app.core.constants import status_messages

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