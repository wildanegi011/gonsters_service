"""InfluxDB connection."""

from influxdb_client_3 import InfluxDBClient3, WriteOptions, write_client_options
from influxdb_client_3.exceptions.exceptions import InfluxDBError

from app.core.setting import settings

# Define the result object
result = {
    'config': None,
    'status': None,
    'data': None,
    'error': None
}

# Define callback for write response
def success_callback(self, data: str):
    """Success callback."""
    result['config'] = self
    result['status'] = 'success'
    result['data'] = data

    assert result['data'] != None, f"Expected {result['data']}"
    print(f"Successfully wrote data: {result['data']}")

def error_callback(self, data: str, exception: InfluxDBError):
    """Error callback."""
    result['config'] = self
    result['status'] = 'error'
    result['data'] = data
    result['error'] = exception

    assert result['status'] == "success", f"Expected {result['error']} to be success for {result['config']}"

def retry_callback(self, data: str, exception: InfluxDBError):
    """Retry callback."""
    result['config'] = self
    result['status'] = 'retry_error'
    result['data'] = data
    result['error'] = exception

    assert result['status'] == "success", f"Expected {result['status']} to be success for {result['config']}"



write_options = WriteOptions(
    batch_size= settings.INFLUXDB_BATCH_SIZE,
    flush_interval= settings.INFLUXDB_FLUSH_INTERVAL,
    jitter_interval= settings.INFLUXDB_JITTER_INTERVAL,
    retry_interval= settings.INFLUXDB_RETRY_INTERVAL,
)

wco = write_client_options(
    success_callback=success_callback,
    error_callback=error_callback,
    retry_callback=retry_callback,
    write_options=write_options
)

client = InfluxDBClient3(
    host=settings.INFLUXDB_URL,
    database=settings.INFLUXDB_BUCKET,
    token=settings.INFLUXDB_TOKEN,
    org=settings.INFLUXDB_ORG,
    write_client_options=wco
)
