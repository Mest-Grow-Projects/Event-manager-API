from typing import Annotated
from fastapi import APIRouter, status, Depends
from .users_service import users_service
from app.schemas.users_schema import (
    UsersResponse,
    UserResponse,
    UpdateUserInfo,
    ChangeRole,
    MessageResponse,
    FilterQuery
)
from ..schemas.auth_schema import SignupSchema

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get(
    "/all",
    status_code=status.HTTP_200_OK,
    summary="Get all users",
    response_model=UsersResponse,
)
async def get_users(filter_query: FilterQuery = Depends()):
    return await users_service.get_all_users(filter_query)

@router.get(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Get user profile",
    response_model=UserResponse,
)
async def get_user_profile(user_id: str):
    return await users_service.get_user_by_id(user_id)

@router.patch(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Update user profile",
    response_model=UserResponse,
)
async def update_user_bio(user_id: str, bio: UpdateUserInfo):
    return await users_service.update_user_by_id(user_id, bio)

@router.delete(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete user profile",
    response_model=MessageResponse,
)
async def delete_user_profile(user_id: str):
    return await users_service.delete_user_by_id(user_id)

@router.post(
    "/add-admin",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new app admin profile",
    response_model=MessageResponse,
)
async def create_admin(user: SignupSchema):
    return await users_service.add_app_admin(user)

@router.post(
    "/add-organizer",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new product admin profile",
    response_model=MessageResponse,
)
async def create_organizer(user: SignupSchema):
    return await users_service.add_organizer(user)

@router.patch(
    "/update_role/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Update user role status",
    response_model=MessageResponse,
)
async def update_user_role(user_id: str, data: ChangeRole):
    return await users_service.change_role_status(user_id, data)