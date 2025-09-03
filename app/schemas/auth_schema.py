from pydantic import BaseModel, EmailStr, Field, model_validator, field_validator
import re
from app.core.constants import validations, patterns_regex

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    sub: str | None = None

class SignupSchema(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=50,
        pattern=patterns_regex["name"],
        description=validations["name"],
    )
    email: EmailStr
    password: str = Field(
        min_length=8,
        description=validations["password"],
    )
    confirm_password: str = Field(
        min_length=8,
        description=validations["password"],
    )

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if not re.search(r"[a-z]", value):
            raise ValueError(validations["lowercase"])
        if not re.search(r"[A-Z]", value):
            raise ValueError(validations["uppercase"])
        if not re.search(r"\d", value):
            raise ValueError(validations["digit"])
        if not re.search(r"[@$!%*?&]", value):
            raise ValueError(validations["special_character"])
        return value

    @model_validator(mode='after')
    def check_password_match(self) -> 'SignupSchema':
        if self.password != self.confirm_password:
            raise ValueError(validations["password_mismatch"])
        return self

    model_config = { "extra": "forbid" }

class LoginSchema(BaseModel):
    email: EmailStr
    password: str = Field(
        min_length=8,
        description=validations["password"],
    )
    model_config = {"extra": "forbid"}

class VerifyAccount(BaseModel):
    code: str = Field(
        min_length=6,
        pattern=patterns_regex["code"],
        description=validations["code"],
    )
    model_config = {"extra": "forbid"}


class SignupResponse(BaseModel):
    message: str
    token: str


class VerifyAccountResponse(BaseModel):
    message: str

class UserResponse(BaseModel):
    name: str
    email: str
    accountStatus: str
    role: str

class Data(BaseModel):
    access_token: str
    user: UserResponse

class LoginResponse(BaseModel):
    message: str
    data: Data