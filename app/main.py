"""Main application."""

import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.lib import mqtt
from app.lib.redis import RedisClient
from app.modules.auth.endpoint import auth_endpoint
from app.modules.ingest.endpoint import ingest_endpoint
from app.modules.machine.endpoint import machine_endpoint

redis_client = RedisClient()

@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Lifespan."""
    await mqtt.fast_mqtt.mqtt_startup()
    await redis_client.connect()
    yield
    await mqtt.fast_mqtt.mqtt_shutdown()
    await redis_client.close()


def create_app() -> FastAPI:
    """Create app."""
    app = FastAPI(
        title="Gonsters Services",
        description="Gonsters Services API",
        version="1.0.0",
        lifespan=lifespan
    )

    # Include routers
    app.include_router(auth_endpoint.router, prefix="/api/v1/auth")
    app.include_router(machine_endpoint.router, prefix="/api/v1/data")
    app.include_router(ingest_endpoint.router, prefix="/api/v1/data")

    return app

app = create_app()

@app.post("/publish_topic")
async def publish_topic():
    """Publish topic."""
    mqtt.fast_mqtt.publish("/factory/A/machine/1/telemetry", {
        "temperature": 25,
        "pressure": 1013,
        "speed": 0,
        "timestamp": "2022-01-01T00:00:00Z"
    })
    return {"result": True, "message": "Published"}
