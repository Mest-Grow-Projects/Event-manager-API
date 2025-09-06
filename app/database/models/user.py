from enum import Enum
from pydantic import EmailStr, Field
from datetime import datetime
from beanie import Document, Indexed
import pymongo
from typing import Annotated

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
    phone: str | None = None
    location: str | None = None
    password: str
    role: Roles = Roles.ATTENDEE
    accountStatus: AccountStatus = AccountStatus.PENDING
    gender: Gender | None = None
    avatar: str | None = None
    dob: datetime | None = None
    bio: str | None = None
    createdAt: datetime = Field(default_factory=datetime.now)
    updatedAt: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = 'users'
        indexes = [
            [("role", pymongo.ASCENDING)],
            [("accountStatus", pymongo.ASCENDING)],
            [("createdAt", pymongo.DESCENDING)],
        ]