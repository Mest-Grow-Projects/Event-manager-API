from http.client import HTTPException
from fastapi import APIRouter, status
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
async def signup_user(user: SignupSchema):
    try:
        return await auth_service.signup(user)
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error
        )

@router.post(
    "/verify-account",
    status_code=status.HTTP_200_OK,
    summary="Verify a user's account with code",
    response_model=VerifyAccountResponse,
)
async def verify_user(data: VerifyAccount, token: str):
    try:
        return await auth_service.verify_account(data, token)
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error
        )

@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    summary="Login a user",
    response_model=LoginResponse
)
async def login_user(user: LoginSchema):
    try:
        return await auth_service.login(user)
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error
        )