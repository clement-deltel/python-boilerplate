"""Module used to customize the format of log messages."""

# Standard Library
from datetime import UTC, datetime
from json import dumps
from logging import Formatter, LogRecord
from typing import Any

# Local Application
from app_name.event.formatter.colors import Colors


class JSONFormatter(Formatter):
    """Class specifying attributes and methods related to log messages serialization in JSON."""

    def __init__(self, app_env: str, level: str, extra_fields: set, color_enabled: bool = False, pretty_json: bool = False) -> None:
        """Initialize class."""
        super().__init__()
        self.app_env = app_env
        self.level = level
        self.extra_fields = extra_fields
        self.color_enabled = color_enabled
        self.pretty_json = pretty_json

        self.colors = {item.name: item.value for item in Colors}
        self.reset = "\x1b[0m"

    def formatTime(self, record: LogRecord, datefmt: str | None = None) -> str:  # noqa: ARG002, N802
        """Format timestamp according to RFC3339 specification.

        Args:
            record (logging.LogRecord): an event being logged.
            datefmt (str): ignored, RFC3339 format is always used.

        Returns:
            str: RFC3339 formatted timestamp
        """
        # Format with microseconds and Z suffix for UTC
        return datetime.fromtimestamp(record.created, tz=UTC).isoformat(timespec="microseconds").replace("+00:00", "Z")

    def format(self, record: LogRecord) -> str:
        """Format record to JSON, and apply colors if enabled.

        Args:
            record (logging.LogRecord): an event being logged.

        Returns:
            str: record formatted as JSON.
        """
        info = record.__dict__.copy()
        message = {}
        message["name"] = info["name"]
        message["environment"] = self.app_env
        message["timestamp"] = self.formatTime(record)
        message["level"] = info["levelname"]
        message["message"] = record.getMessage()

        # Handle exception (if any) information formatting
        if record.exc_info and record.exc_text is None:
            message["exc_info"] = self.formatException(record.exc_info)
        # Handle stack (if any) information formatting
        if record.stack_info:
            message["stack_info"] = self.formatStack(record.stack_info)
        # Handle extra
        for field in self.extra_fields:
            if field in info:
                message[field] = info[field]
        # Add more context in a debugging scenario
        if self.level == "DEBUG":
            message["module"] = record.module
            message["function"] = record.funcName
            message["lineno"] = record.lineno

        # Improve JSON readability
        pretty_options: dict[str, Any] = {}
        if self.pretty_json:
            pretty_options["indent"] = 2

        # Apply color if enabled
        if self.color_enabled:
            color = self.colors[record.levelname]
            log_message = color + dumps(message, **pretty_options) + self.reset
        else:
            log_message = dumps(message, **pretty_options)

        return log_message
