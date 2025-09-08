from fastapi import APIRouter, status, BackgroundTasks
from .auth_service import auth_service
from app.schemas.auth_schema import (
    SignupSchema,
    LoginSchema,
    VerifyAccount,
    SignupResponse,
    LoginResponse,
    VerifyAccountResponse
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post(
    "/signup",
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    response_model=SignupResponse
)
async def signup_user(user: SignupSchema, background_tasks: BackgroundTasks):
    return await auth_service.signup(user, background_tasks)

@router.post(
    "/verify-account",
    status_code=status.HTTP_200_OK,
    summary="Verify a user's account with code",
    response_model=VerifyAccountResponse,
)
async def verify_user(data: VerifyAccount, token: str, background_tasks: BackgroundTasks):
    return await auth_service.verify_account(data, token, background_tasks)

@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    summary="Login a user",
    response_model=LoginResponse
)
async def login_user(user: LoginSchema):
    return await auth_service.login(user)