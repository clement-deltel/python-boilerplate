#!/usr/bin/env python3
"""Module used to customize the format of log messages."""

# Standard Library
from datetime import UTC, datetime
from logging import Formatter, LogRecord

# Local Application
from app_name.event.formatter.colors import Colors


class CustomFormatter(Formatter):
    """Class specifying attributes and methods related to log messages custom formatting."""

    def __init__(self, app_env: str, level: str, extra_fields: set, color_enabled: bool = False):
        """Initialize class."""
        super().__init__()
        self.app_env = app_env
        self.level = level
        self.extra_fields = extra_fields
        self.color_enabled = color_enabled

        self.colors = {item.name: item.value for item in Colors}
        self.fmt = "%(asctime)-20s - %(levelname)-8s - %(message)s"
        self.reset = "\x1b[0m"

    def formatTime(self, record: LogRecord, datefmt=None):  # noqa: ARG002, N802
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
        """Retrieve extra information and apply different colors to the log messages.

        Args:
            record (logging.LogRecord): an event being logged.

        Returns:
            str: record formatted as text.
        """
        info = record.__dict__.copy()
        message = self.fmt.split("%")
        # Handle extra
        for field in self.extra_fields:
            if field in info:
                message[-1] += " - "
                message.append(f"({field})s")
        fmt = "%".join(message)
        fmt = f"{self.app_env} - {fmt}"
        # Add more context in a debugging scenario
        if self.level == "DEBUG":
            fmt = f"{fmt} (%(module)s::%(funcName)s:%(lineno)s)"

        # Apply color if enabled
        if self.color_enabled:
            color = self.colors[record.levelname]
            log_fmt = color + fmt + self.reset
        else:
            log_fmt = fmt

        return Formatter(log_fmt, self.datefmt).format(record)
