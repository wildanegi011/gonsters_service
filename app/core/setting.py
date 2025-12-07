"""Settings."""

from pydantic_settings import BaseSettings

from app.utils.env import env


class Settings(BaseSettings):
    """Initialize Settings."""

    DATABASE_URL: str = env.database_url
    INFLUXDB_BUCKET: str = env.influxdb_bucket
    INFLUXDB_URL: str = env.influxdb_url
    INFLUXDB_TOKEN: str = env.influxdb_token
    INFLUXDB_ORG: str = env.influxdb_org
    INFLUXDB_BATCH_SIZE: int = env.influxdb_batch_size
    INFLUXDB_FLUSH_INTERVAL: int = env.influxdb_flush_interval
    INFLUXDB_JITTER_INTERVAL: int = env.influxdb_jitter_interval
    INFLUXDB_RETRY_INTERVAL: int = env.influxdb_retry_interval

    REDIS_HOST: str = env.redis_host
    REDIS_PORT: int = env.redis_port
    REDIS_DB: int = env.redis_db
    REDIS_EXPIRE: int = env.redis_expire


settings = Settings()
