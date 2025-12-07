"""MQTT lib."""

import json
from typing import Any

from fastapi_mqtt import FastMQTT, MQTTClient, MQTTConfig

from app.utils.logging import DevLogger

logger = DevLogger("mqtt").get()

mqtt_config = MQTTConfig(
    host="emqx",
)
fast_mqtt = FastMQTT(config=mqtt_config)

@fast_mqtt.on_connect()
def connect(client: MQTTClient, flags: int, rc: int, properties: Any):
    """Connect."""
    client.subscribe("/factory/A/machine/+/telemetry")
    logger.info(f"Connected: {client}, {flags}, {rc}, {properties}")

@fast_mqtt.on_message()
async def message(client: MQTTClient, topic: str, payload: bytes, qos: int, properties: Any):
    """Message."""
    payload_str = payload.decode()
    try:
        data = json.loads(payload_str)
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON received on {topic}: {payload_str}")
        return

    logger.info(f"Processed message on {topic}: {data}")

@fast_mqtt.on_disconnect()
def disconnect(client: MQTTClient, rc: int, properties: Any):
    """Disconnect."""
    client.disconnect()
    logger.info("Disconnected")
