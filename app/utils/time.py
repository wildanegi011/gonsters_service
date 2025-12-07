"""Datetime utils."""

from datetime import UTC, datetime


def now_utc() -> datetime:
    """Get current UTC time."""
    return datetime.now(UTC)
