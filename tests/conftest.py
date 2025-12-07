"""Pytest configuration and fixtures."""
import os
import sys
from unittest.mock import MagicMock

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Set up test environment variables with default values
test_env_vars = {
    # Database
    "DATABASE_URL": "sqlite:///:memory:",
    "DATABASE_TEST_URL": "sqlite:///:memory:",

    # InfluxDB
    "INFLUXDB_URL": "http://test-influx:8086",
    "INFLUXDB_TOKEN": "test-token",
    "INFLUXDB_ORG": "test-org",
    "INFLUXDB_BUCKET": "test-bucket",
    "INFLUXDB_BATCH_SIZE": "1000",
    "INFLUXDB_FLUSH_INTERVAL": "1",
    "INFLUXDB_JITTER_INTERVAL": "1",
    "INFLUXDB_RETRY_INTERVAL": "1",

    # Redis
    "REDIS_URL": "redis://localhost:6379/0",
    "REDIS_EXPIRE": "60",
    "REDIS_DB": "0",
    "REDIS_HOST": "localhost",
    "REDIS_PORT": "6379",
    "REDIS_PASSWORD": "",
    "REDIS_USERNAME": "",

    # JWT
    "JWT_SECRET_KEY": "test-secret-key",
    "JWT_ALGORITHM": "HS256",
    "JWT_ACCESS_TOKEN_EXPIRE_MINUTES": "30",

    # Application
    "ENVIRONMENT": "test",
    "DEBUG": "True",
    "LOG_LEVEL": "INFO",

    # CORS
    "CORS_ORIGINS": "http://localhost:3000,http://localhost:8000",

    # API
    "API_PREFIX": "/api/v1",
    "API_KEY": "test-api-key"
}

# Apply environment variables
for key, value in test_env_vars.items():
    os.environ.setdefault(key, value)

# Mock the influxdb client
mock_influx_client = MagicMock()

# Apply the mock before any tests run
import app.db.influx_db  # noqa: E402

app.db.influx_db.client = mock_influx_client
