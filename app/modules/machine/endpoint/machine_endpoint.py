"""Machine Endpoint."""

from typing import Annotated, Any

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.modules.machine.schema.machine_schema import MachineSchema, SensorData
from app.modules.machine.service.machine_service import MachineService
from app.utils.base_response import BaseResponse

router = APIRouter(
    prefix="/machine",
    tags=["machines"],
)

def get_machine_service(db: Annotated[Session, Depends(get_db)]):
    """Get machine service."""
    return MachineService(db)


@router.post("", response_model=BaseResponse)
async def create_machine(schema: MachineSchema, service: Annotated[MachineService, Depends(get_machine_service)],):
    """Create machine."""
    response = await service.create_machine(schema)
    return BaseResponse(status=True, message="successfully creating machine", data=response)


@router.get("/{machine_id}", response_model=BaseResponse[list[dict[str, Any]]])
async def get_machines(
    machine_id: int,
    service: Annotated[MachineService, Depends(get_machine_service)],
    start_time: str = Query(..., example="2025-01-10T00:00:00Z"),
    end_time: str = Query(..., example="2025-01-10T23:59:59Z"),
    interval: str = Query(None, example="5m"),
):
    """Get machines."""
    response = await service.get_machine(machine_id, start_time, end_time, interval)
    return BaseResponse(status=True, message="successfully fetching data", data=response)
