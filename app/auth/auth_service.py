from fastapi import HTTPException, status
from app.core.constants import validations, success_messages, status_messages
from app.schemas.auth_schema import SignupSchema, LoginSchema, VerifyAccount
from app.models.user import User, AccountStatus
from app.database.repo.user_repo import check_existing_user, find_user_by_email
from app.utils.auth_utils import (
    generate_verification_code,
    get_password_hash,
    verify_password,
    create_access_token
)
from datetime import timedelta, datetime, timezone
from app.core.config import get_settings
import jwt

secret = get_settings().SECRET_KEY

class AuthService:
    def __init__(self, secret_key: str, jwt_algorithm: str = "HS256"):
        self.secret_key = secret_key
        self.jwt_algorithm = jwt_algorithm
        self.signup_token_duration = timedelta(minutes=30)

    async def signup(self, user: SignupSchema):
        await check_existing_user(str(user.email))
        verification_code = generate_verification_code()
        hashed_password = get_password_hash(user.password)

        new_user = User(
            name=user.name,
            email=user.email,
            password=hashed_password
        )
        await new_user.insert()

        payload = {
            "sub": str(user.email),
            "code": verification_code,
            'exp': datetime.now(timezone.utc) + self.signup_token_duration,
        }
        token = jwt.encode(payload, self.secret_key, algorithm=self.jwt_algorithm)

        return {
            'message': success_messages['signup'],
            'data': {
                'token': token,
                'verification_code': verification_code,
            },
        }


    async def verify_account(self, data: VerifyAccount, token: str):
        if not data.code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=status_messages["code_required"],
            )

        try:
            decoded_token = jwt.decode(token, self.secret_key, algorithms=[self.jwt_algorithm])
            email = decoded_token.get('sub')
            token_code = decoded_token.get('code')

            if not email or not token_code:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=validations["token_required"],
                )

            if 'exp' in decoded_token and datetime.now(timezone.utc).timestamp() > decoded_token['exp']:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=validations["invalid_token"],
                )

            if data.code != token_code:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=validations["invalid_code"],
                )

            user = await find_user_by_email(email)
            if user.accountStatus == AccountStatus.VERIFIED:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=validations["already_verified"],
                )

            user.accountStatus = AccountStatus.VERIFIED
            await user.save()

            return { "message": success_messages["verify_account"] }
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=validations["invalid_token"],
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=validations["invalid_token"],
            )


    async def login(self, user: LoginSchema):
        found_user = await find_user_by_email(str(user.email))
        password_valid = verify_password(user.password, found_user.password)

        if found_user.accountStatus != AccountStatus.VERIFIED:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=validations["not_verified"],
            )

        if not found_user or not password_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=validations["invalid_credentials"]
            )

        access_token = create_access_token(
            data={
                "sub": str(found_user.email),
                "name": found_user.name,
                "role": found_user.role,
                "accountStatus": found_user.accountStatus,
            }
        )
        return {
            "message": success_messages['login'],
            "data": {
                "access_token": access_token,
                "user": {
                    "name": found_user.name,
                    "email": found_user.email,
                    "role": found_user.role,
                    "accountStatus": found_user.accountStatus,
                }
            }
        }

auth_service = AuthService(secret_key=secret)