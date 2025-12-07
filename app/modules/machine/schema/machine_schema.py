"""Machine Schema."""

from pydantic import BaseModel

from app.modules.machine.model.machine_model import StatusEnum


class MachineSchema(BaseModel):
    """Machine create schema."""

    name: str
    location: str
    sensor_type: str
    status: StatusEnum


class SensorData(BaseModel):
    """Sensor data schema."""

    machine_id: int
    temperature: float
    pressure: float
    speed: float
