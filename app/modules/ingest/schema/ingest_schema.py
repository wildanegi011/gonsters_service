"""Ingest Schema."""


from datetime import datetime

from pydantic import BaseModel, Field


class Record(BaseModel):
    """Record."""

    timestamp: datetime
    temperature: float | None = None
    pressure: float | None = None
    speed: float | None = None

class IngestSchema(BaseModel):
    """Ingest Schema."""

    machine_id: int
    sensor_data: list[Record] = Field(min_length=1)
