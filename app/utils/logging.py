"""Logging configuration."""

import json
import logging
from datetime import datetime
from typing import Any


class ColoredFormatter(logging.Formatter):
    """Console formatter with color output (dev only)."""

    COLORS = {
        "DEBUG": "\033[36m",
        "INFO": "\033[32m",
        "WARNING": "\033[33m",
        "ERROR": "\033[31m",
        "CRITICAL": "\033[1;31m",
    }
    RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        """Format."""
        colored_level = f"{self.COLORS.get(record.levelname, self.RESET)}{record.levelname}{self.RESET}"
        colored_msg = f"{self.COLORS.get(record.levelname, self.RESET)}{record.getMessage()}{self.RESET}"

        # use a copy of the record to avoid modifying shared state
        record_copy = logging.LogRecord(
            name=record.name,
            level=record.levelno,
            pathname=record.pathname,
            lineno=record.lineno,
            msg=colored_msg,
            args=record.args,
            exc_info=record.exc_info,
        )
        record_copy.levelname = colored_level
        record_copy.created = record.created

        return super().format(record_copy)


class JSONFormatter(logging.Formatter):
    """File formatter that outputs structured JSON logs."""

    def format(self, record: logging.LogRecord) -> str:
        """Format."""
        log: dict[str, Any] = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "file": record.pathname,
            "line": record.lineno
        }

        # add exception info
        if record.exc_info:
            log["exception"] = self.formatException(record.exc_info)

        return json.dumps(log, ensure_ascii=False)


class DevLogger:
    """Custom dev logger with optional file output in JSON."""

    def __init__(
        self,
        name: str = "dev-env",
        level: int | None = logging.DEBUG,
        to_file: bool = False,
        log_path: str = "logs/dev.log",
    ):
        """Initialize."""
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level or logging.DEBUG)

        if not self.logger.handlers:
            # ───────────────────────────────────────────────
            # Console logging (colored)
            # ───────────────────────────────────────────────
            color_fmt = "🛠️ [DEV] %(asctime)s — %(levelname)s — %(message)s"
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(
                ColoredFormatter(color_fmt, datefmt="%H:%M:%S")
            )
            self.logger.addHandler(stream_handler)

            # ───────────────────────────────────────────────
            # Optional file logging (JSON)
            # ───────────────────────────────────────────────
            if to_file:
                file_handler = logging.FileHandler(log_path)
                file_handler.setFormatter(JSONFormatter())
                self.logger.addHandler(file_handler)

    def get(self) -> logging.Logger:
        """Get logger."""
        return self.logger
