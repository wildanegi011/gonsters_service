"""Pytest configuration and fixtures."""
import os
import sys
from unittest.mock import MagicMock

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Set up test environment variables
os.environ["INFLUXDB_URL"] = "http://test-influx:8086"
os.environ["INFLUXDB_TOKEN"] = "test-token"
os.environ["INFLUXDB_ORG"] = "test-org"
os.environ["INFLUXDB_BUCKET"] = "test-bucket"

# Mock the influxdb client
mock_influx_client = MagicMock()

# Apply the mock before any tests run
import app.db.influx_db  # noqa: E402

app.db.influx_db.client = mock_influx_client
