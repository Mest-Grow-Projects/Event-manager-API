from pydantic import BaseModel, Field
from datetime import datetime, timezone

class TimestampMixin(BaseModel):
    createdAt: datetime = Field(default_factory=datetime.now(timezone.utc))
    updatedAt: datetime = Field(default_factory=datetime.now(timezone.utc))