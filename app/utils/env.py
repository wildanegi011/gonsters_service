"""Centralized environment configuration.

This module loads environment variables once and provides typed access
to prevent multiple load_dotenv() calls across the codebase.

Key Benefits:
- Single load_dotenv() call (instead of 6+ scattered calls)
- Typed access with proper defaults
- Clear separation between production and development variables
- Built-in validation helpers for deployment readiness
- Strict validation using get_env_var pattern for required variables
"""

import os

from dotenv import load_dotenv

load_dotenv()

class EnvConfig:
    """Centralized environment configuration."""

    def get_env_var(self, name: str, default: str | None = None) -> str:
        """Get an environment variable or return a default value.

        This method provides strict validation - raises ValueError if required
        environment variables are missing.

        Args:
            name: The name of the environment variable
            default: Optional default value if the environment variable is not set

        Returns:
            The value of the environment variable

        Raises:
            ValueError: If the environment variable is not set and no default is provided

        """
        value = os.environ.get(name)
        if value is None:
            if default is None:
                raise ValueError(f"Environment variable {name} is not set and no default provided")
            else:
                print(f"Environment variable {name} is not set, using default value: {default}")
                return default
        return value

    #-----------------------------------------------------
    # Database Configuration
    #-----------------------------------------------------
    @property
    def database_url(self) -> str:
        """Get database url."""
        return self.get_env_var("DATABASE_URL")

    #-----------------------------------------------------
    # InfluxDB Configuration
    #-----------------------------------------------------
    @property
    def influxdb_url(self) -> str:
        """Get influxdb url."""
        return self.get_env_var("INFLUXDB_URL")

    @property
    def influxdb_token(self) -> str:
        """Get influxdb token."""
        return self.get_env_var("INFLUXDB_TOKEN")

    @property
    def influxdb_org(self) -> str:
        """Get influxdb org."""
        return self.get_env_var("INFLUXDB_ORG")

    @property
    def influxdb_bucket(self) -> str:
        """Get influxdb bucket."""
        return self.get_env_var("INFLUXDB_BUCKET", "test-bucket")

    @property
    def influxdb_batch_size(self) -> int:
        """Get influxdb batch size."""
        return int(self.get_env_var("INFLUXDB_BATCH_SIZE", "1"))

    @property
    def influxdb_flush_interval(self) -> int:
        """Get influxdb flush interval."""
        return int(self.get_env_var("INFLUXDB_FLUSH_INTERVAL", "1"))

    @property
    def influxdb_jitter_interval(self) -> int:
        """Get influxdb jitter interval."""
        return int(self.get_env_var("INFLUXDB_JITTER_INTERVAL", "1"))

    @property
    def influxdb_retry_interval(self) -> int:
        """Get influxdb retry interval."""
        return int(self.get_env_var("INFLUXDB_RETRY_INTERVAL", "1"))

    #-----------------------------------------------------
    # Redis Configuration
    #-----------------------------------------------------
    @property
    def redis_host(self) -> str:
        """Get redis host."""
        return self.get_env_var("REDIS_HOST")

    @property
    def redis_port(self) -> int:
        """Get redis port."""
        return int(self.get_env_var("REDIS_PORT", "6379"))

    @property
    def redis_db(self) -> int:
        """Get redis db."""
        return int(self.get_env_var("REDIS_DB", "0"))

    @property
    def redis_expire(self) -> int:
        """Get redis expire."""
        return int(self.get_env_var("REDIS_EXPIRE", "60"))


env = EnvConfig()
