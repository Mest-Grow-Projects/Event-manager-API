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

class User(Document):
    name: str
    email: Annotated[EmailStr, Indexed(unique=True)]
    phone: str | None
    location: str | None
    password: str
    role: Roles = Roles.ATTENDEE
    createdAt: datetime = Field(default_factory=datetime.now())
    updatedAt: datetime = Field(default_factory=datetime.now())

    class Settings:
        name = 'users'
        indexes = [
            [("email", pymongo.ASCENDING)],
            [("role", pymongo.ASCENDING)],
            [("createdAt", pymongo.DESCENDING)],
        ]