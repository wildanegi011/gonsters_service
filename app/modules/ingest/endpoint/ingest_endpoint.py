""""Ingest Endpoint."""


from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.modules.ingest.schema.ingest_schema import IngestSchema
from app.modules.ingest.service.ingest_service import IngestService

router = APIRouter(
        tags=["Ingest"],
        prefix="/ingest"
)

def get_ingest_service(db: Annotated[Session, Depends(get_db)]):
    """Get ingest service."""
    return IngestService(db)

@router.post("")
async def ingest_data(schema: IngestSchema, service: Annotated[IngestService, Depends(get_ingest_service)]):
    """Ingest data."""
    await service.ingest_data(schema)
    return {"status": True, "message": "successfully ingesting data"}
