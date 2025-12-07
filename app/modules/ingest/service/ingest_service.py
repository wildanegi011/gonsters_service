"""Ingest Service."""

from sqlalchemy.orm import Session

from app.core.setting import settings
from app.db.influx_db import client
from app.modules.ingest.schema.ingest_schema import IngestSchema
from app.modules.machine.service.machine_service import MachineService
from app.utils.logging import DevLogger

logger = DevLogger("ingest_service", to_file=True).get()

class IngestService:
    """Initialize Ingest service."""

    def __init__(self, db: Session):
        """Initialize constructor."""
        self.db = db
        self.machine_service = MachineService(db)

    async def ingest_data(self, schema: IngestSchema):
        """Ingest data."""
        self.machine_service.fetch_machine(schema.machine_id)
        logger.debug({"payload": schema.model_dump()})

        lines = []
        for r in schema.sensor_data:
            lines.append(
                f"machine_sensor_data,"
                f"machine_id={schema.machine_id} "
                f"temperature={r.temperature},pressure={r.pressure},speed={r.speed} "
                f"{int(r.timestamp.timestamp() * 1e9)}"
            )

        client.write(database=settings.INFLUXDB_BUCKET, record=lines)
        return lines

