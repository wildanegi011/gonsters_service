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
        expire: int = settings.REDIS_EXPIRE,
    ):
        """Initialize Redis client settings."""
        self._host = host
        self._port = port
        self._db = db
        self._expire = expire
        self._client: redis.Redis | None = None

    async def connect(self) -> redis.Redis:
        """Establish a connection to the Redis server."""
        if self._client is None:
            try:
                self._client = redis.Redis(
                    host=self._host,
                    port=self._port,
                    db=self._db,
                    decode_responses=True,
                    socket_timeout=5,
                    retry_on_timeout=True,
                )

                await self._client.ping()
                logger.info(f"Connected to Redis at {self._host}:{self._port}/{self._db}")
            except (ConnectionError, TimeoutError, RedisError) as e:
                logger.error(f"Failed to connect to Redis: {e}")
                raise

        return self._client

    async def close(self) -> None:
        """Close the Redis connection."""
        if self._client:
            try:
                await self._client.close()
                logger.info("Redis connection closed.")
            except Exception as e:
                logger.warning(f"Failed to close Redis connection: {e}")
            finally:
                self._client = None

    async def _get_client(self) -> redis.Redis:
        if self._client is None:
            return await self.connect()
        return self._client

    async def get(self, key: str) -> dict | list | str | None:
        """Get the value of a key from Redis."""
        client = await self._get_client()
        try:
            value = await client.get(key)
            if value is None:
                return None

            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value

        except RedisError as e:
            logger.error(f"Redis GET error for key '{key}': {e}")
            return None

    async def set(self, key: str, value, expire: int | None = None) -> bool:
        """Set key with auto JSON encoding and optional expire."""
        client = await self._get_client()
        try:
            json_value = json.dumps(value)
            exp: int = expire or self._expire
            success = await client.set(key, json_value, ex=exp)
            return bool(success)
        except RedisError as e:
            logger.error(f"Redis SET error for key '{key}': {e}")
            return False

    async def delete(self, key: str) -> bool:
        """Delete a key."""
        client = await self._get_client()
        try:
            deleted = await client.delete(key)
            return bool(deleted)
        except RedisError as e:
            logger.error(f"Redis DELETE error for key '{key}': {e}")
            return False
