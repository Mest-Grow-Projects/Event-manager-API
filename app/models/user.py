from enum import Enum
from typing import Annotated
from pydantic import EmailStr, Field
from datetime import datetime
from beanie import Document, Indexed
import pymongo

class Roles(str, Enum):
    ATTENDEE = "ATTENDEE"
    ORGANIZER = "ORGANIZER"
    ADMIN = "ADMIN"

class AccountStatus(str, Enum):
    VERIFIED = "VERIFIED"
    PENDING = "PENDING"
    SUSPENDED = "SUSPENDED"

class Gender(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    NON_BINARY = "NON_BINARY"

class User(Document):
    name: str
    email: Annotated[EmailStr, Indexed(unique=True)]
    phone: str | None
    location: str | None
    password: str
    role: Roles = Roles.ATTENDEE
    accountStatus: AccountStatus = AccountStatus.PENDING
    gender: Gender | None
    avatar: str | None
    dob: datetime | None
    createdAt: datetime = Field(default_factory=datetime.now())
    updatedAt: datetime = Field(default_factory=datetime.now())

    class Settings:
        name = 'users'
        indexes = [
            [("role", pymongo.ASCENDING)],
            [("accountStatus", pymongo.ASCENDING)],
            [("createdAt", pymongo.DESCENDING)],
        ]