"""Machine Model."""

from datetime import datetime
from enum import Enum

from sqlmodel import Field, SQLModel

from app.utils.time import now_utc


class StatusEnum(str, Enum):
    """Status enum."""

    active = "active"
    inactive = "inactive"
    maintenance = "maintenance"


class Machine(SQLModel, table=True):
    """Initialize machine model."""

    __tablename__ = "machine_metadata"

    id: int = Field(primary_key=True)
    name: str = Field(nullable=False, max_length=100)
    location: str = Field(nullable=False, max_length=100, index=True)
    sensor_type: str = Field(nullable=False, max_length=50, index=True)
    status: StatusEnum = Field(nullable=False)
    created_at: datetime = Field(default_factory=now_utc)
    updated_at: datetime = Field(default_factory=now_utc)
