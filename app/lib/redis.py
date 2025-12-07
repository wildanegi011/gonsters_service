"""Redis client library."""

import json

import redis.asyncio as redis
from redis.exceptions import RedisError

from app.core.setting import settings
from app.utils.logging import DevLogger

logger = DevLogger("redis", to_file=True).get()


class RedisClient:
    """Async Redis client with context management."""

    def __init__(
        self,
        host: str = settings.REDIS_HOST,
        port: int = settings.REDIS_PORT,
        db: int = settings.REDIS_DB,
    ):
        """Initialize Redis client settings."""
        self._host = host
        self._port = port
        self._db = db
        self._client: redis.Redis | None = None

    async def connect(self) -> None:
        """Establish a connection to the Redis server."""
        if self._client is None:
            self._client = redis.Redis(
                host=self._host,
                port=self._port,
                db=self._db,
                decode_responses=True
            )
        try:
            await self._client.ping()
            logger.info(f"Connected to Redis at {self._host}:{self._port}/{self._db}")
        except RedisError as e:
            logger.warning(f"Redis connection failed: {e}")
            raise

    async def close(self) -> None:
        """Close the Redis connection."""
        if self._client:
            await self._client.close()
            self._client = None
            logger.info("Redis connection closed.")

    async def get(self, key: str) -> str | None:
        """Get the value of a key from Redis."""
        if not self._client:
            logger.info("Redis not connected, connecting now...")
            await self.connect()
        try:
            return await self._client.get(key)
        except RedisError as e:
            logger.error(f"Failed to get key '{key}': {e}")
            return None

    async def set(self, key: str, value: list, expire: int = settings.REDIS_EXPIRE) -> bool:  # noqa: UP007
        """Set a key-value pair in Redis with optional expiration (seconds)."""
        if not self._client:
            logger.info("Redis not connected, connecting now...")
            await self.connect()
        try:
            json_value = json.dumps(value)
            return await self._client.set(key, json_value, ex=expire)
        except RedisError as e:
            logger.error(f"Failed to set key '{key}': {e}")
            return False

    async def delete(self, key: str) -> bool:
        """Delete a key from Redis."""
        if not self._client:
            logger.info("Redis not connected, connecting now...")
            await self.connect()
        try:
            deleted = await self._client.delete(key)
            return bool(deleted)
        except RedisError as e:
            logger.error(f"Failed to delete key '{key}': {e}")
            return False
