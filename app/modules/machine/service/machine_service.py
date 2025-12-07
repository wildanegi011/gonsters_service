"""Machine Service."""

import json

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db.influx_db import client
from app.lib.redis import RedisClient
from app.modules.machine.model.machine_model import Machine
from app.modules.machine.schema.machine_schema import MachineSchema
from app.utils.logging import DevLogger

logger = DevLogger(name="machine_service", to_file=True).get()

redis_client = RedisClient()  # shared instance

class MachineService:
    """Machine Service."""

    def __init__(self, db: Session) -> None:
        """Initialize."""
        self.db = db

    def fetch_machine(self, machine_id: int):
        """Fetch machine."""
        machine = self.db.query(Machine).filter(Machine.id == machine_id).first()
        if not machine:
            raise HTTPException(status_code=404, detail="Machine not found")


    async def get_machine(self, machine_id: int, start_time: str, end_time: str, interval: str = None):
        """Get machines."""
        # check machine
        self.fetch_machine(machine_id)

        # check redis
        redis_key = f"machine:{machine_id}:data:{start_time}:{end_time}:{interval}"
        redis_data = await redis_client.get(redis_key)
        if redis_data:
            return json.loads(redis_data)

        logger.debug({"payload": {"machine_id": machine_id, "start_time": start_time, "end_time": end_time, "interval": interval}})  # noqa: E501

        if interval:
            time_column = f"date_bin('{interval}', time)::varchar AS time"
            select_fields = """
                AVG(temperature) AS temperature,
                AVG(pressure) AS pressure,
                AVG(speed) AS speed
            """
            group_by = f"GROUP BY date_bin('{interval}', time)"
            order_by = f"ORDER BY date_bin('{interval}', time) DESC"
        else:
            time_column = "time::varchar AS time"
            select_fields = """
                temperature,
                pressure,
                speed
            """
            group_by = ""
            order_by = "ORDER BY time Desc"

        sql = f"""
            SELECT
                {time_column},
                {select_fields}
            FROM machine_sensor_data
            WHERE time >= '{start_time}'
            AND time <= '{end_time}'
            AND machine_id = {machine_id}
            {group_by}
            {order_by}
        """

        table = client.query(sql)
        await redis_client.set(redis_key, table.to_pylist())
        return table.to_pylist()


    async def create_machine(self, schema: MachineSchema) -> Machine:
        """Create machine."""
        logger.debug({"payload": schema.model_dump()})
        machine = Machine(**schema.model_dump())
        self.db.add(machine)
        self.db.commit()
        self.db.refresh(machine)
        return machine
