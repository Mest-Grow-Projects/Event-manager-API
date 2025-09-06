from datetime import datetime
import pymongo
from beanie import Document, Indexed, Link
from pydantic import BaseModel, Field, field_validator
from typing import Annotated, List
from app.database.models.base_mixin import TimestampMixin
from app.database.models.user import User
from enum import Enum


class Address(BaseModel):
    street: str = Field(min_length=2, max_length=50)
    city: str = Field(min_length=2, max_length=50)
    state: str = Field(min_length=2, max_length=50)
    country: str = Field(min_length=2, max_length=50)

    class Config:
        str_strip_whitespace = True

class Location(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    address: Address

class EventStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    CANCELLED = "cancelled"
    COMPLETED = "completed"

class EventCategory(str, Enum):
    CONFERENCE = "conference"
    WORKSHOP = "workshop"
    SEMINAR = "seminar"
    CONCERT = "concert"
    SPORTS = "sports"
    NETWORKING = "networking"
    EXHIBITION = "exhibition"
    WEBINAR = "webinar"
    OTHER = "other"


class Events(Document, TimestampMixin):
    title: Annotated[str, Indexed()] = Field(min_length=5, max_length=50)
    description: str = Field(min_length=10, max_length=1000)
    short_description: str = Field(min_length=10, max_length=255)
    organizer: Link[User]
    category: Annotated[EventCategory, Indexed()]
    location: Location | None = None
    tags: List[str] | None = None
    is_online: bool = Field(default=False)
    meeting_url: str | None = None
    banner_image: str | None = None
    status: EventStatus = Field(default=EventStatus.DRAFT, index=True)
    start_datetime: Annotated[datetime, Indexed()]
    end_datetime: datetime

    @field_validator('end_datetime')
    @classmethod
    def validate_end_datetime(cls, v, values):
        if 'start_datetime' in values and v <= values['start_datetime']:
            raise ValueError('end_datetime must be after start_datetime')
        return v

    class Settings:
        name = 'events'
        indexes = [
            [("organizer_id", pymongo.ASCENDING), ("start_datetime", pymongo.ASCENDING)],
            [("category", pymongo.ASCENDING), ("start_datetime", pymongo.ASCENDING)],
            [("createdAt", pymongo.DESCENDING)],
        ]