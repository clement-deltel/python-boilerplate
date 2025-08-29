#!/usr/bin/env python3
"""Module used to log all the events of the application execution.

Typical usage example:
  Log().open_stream()
  Log().set_level(args.log_level)
  Log().close_stream()
"""

# Standard Library
import logging
from datetime import UTC, datetime
from enum import Enum
from json import dumps
from sys import stderr, stdout
from typing import Any

# Local Application
from app_name.common.config import LogConfig, get_config_class, get_config_value
from app_name.event.cloudevents_formatter import CloudEventsFormatter
from app_name.event.colors import Colors


class Log:
    """Class specifying attributes and methods related to logging."""

    def __init__(self):
        """Initialize class."""
        self.config: LogConfig = get_config_class("log")
        self.levels = {item.name: item.value for item in Levels}

        self.extra_fields = {"user_id", "table", "record", "wait"}

        # Logger
        self._logger = logging.getLogger(get_config_value("app", "name"))
        # Formatters
        self.file_formatter = None
        self.stream_formatter = None
        # Handlers
        self.file_handler = None
        self.stream_handler_out = None
        self.stream_handler_err = None

        self.initialize()

    @property
    def logger(self):
        """Getter method for the attribute _logger."""
        return self._logger

    def initialize(self):
        """."""
        self.set_level(self.config.level)
        self.set_formatters(self.config.level)
        self.open_stream()

        if self.config.to_file:
            self.open_file(str(self.config.file_path))
        else:
            self.open_stream()

    def set_level(self, level: str) -> None:
        """Set log level.

        Args:
            level (str): log level.
        """
        self._logger.setLevel(self.levels[level])

    def set_formatters(self, level: str) -> None:
        """Set formatters.

        Args:
            level (str): log level.
        """
        # Default
        self.file_formatter = CustomFormatter(self.config.app_env, level, self.extra_fields)
        self.stream_formatter = CustomFormatter(self.config.app_env, level, self.extra_fields, self.config.color)
        # JSON formatter
        if self.config.json:
            self.stream_formatter = JSONFormatter(self.config.app_env, level, self.extra_fields, self.config.color, self.config.pretty)
        # CloudEvents formatter
        if self.config.cloudevents:
            self.stream_formatter = CloudEventsFormatter(self.config.app_env, level, self.extra_fields, self.config.color, self.config.pretty)

    def close(self) -> None:
        """Close both stream and file handlers."""
        self.close_file()
        self.close_stream()

    def open_stream(self) -> None:
        """Open the stream handlers to write log messages to stdout and stderr."""
        if self.stream_handler_out is None:
            self.stream_handler_out = logging.StreamHandler(stream=stdout)
            self.stream_handler_out.setFormatter(self.stream_formatter)
            self.stream_handler_out.setLevel(self.levels["DEBUG"])
            self.stream_handler_out.addFilter(ErrFilter())
            self._logger.addHandler(self.stream_handler_out)
        if self.stream_handler_err is None:
            self.stream_handler_err = logging.StreamHandler(stream=stderr)
            self.stream_handler_err.setFormatter(self.stream_formatter)
            self.stream_handler_err.setLevel(self.levels["ERROR"])
            self._logger.addHandler(self.stream_handler_err)

    def close_stream(self) -> None:
        """Close the stream handlers."""
        if self.stream_handler_out is not None:
            self._logger.removeHandler(self.stream_handler_out)
            self.stream_handler_out.close()
            self.stream_handler_out = None
        if self.stream_handler_err is not None:
            self._logger.removeHandler(self.stream_handler_err)
            self.stream_handler_err.close()
            self.stream_handler_err = None

    def open_file(self, file_path: str) -> None:
        """Open the file handler to write log messages to the log file."""
        try:
            if self.file_handler is None:
                self.file_handler = logging.FileHandler(filename=file_path, mode="a", encoding="utf-8")
                self.file_handler.setFormatter(self.file_formatter)
                self.file_handler.setLevel(self.levels["DEBUG"])
                self._logger.addHandler(self.file_handler)
        except FileNotFoundError:
            pass

    def close_file(self) -> None:
        """Close the file handler."""
        if self.file_handler is not None:
            self._logger.removeHandler(self.file_handler)
            self.file_handler.close()
            self.file_handler = None


class CustomFormatter(logging.Formatter):
    """Class used to retrieve extra and set colors for log messages."""

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

    def formatTime(self, record: logging.LogRecord, datefmt=None):  # noqa: ARG002, N802
        """Format timestamp according to RFC3339 specification.

        Args:
            record (logging.LogRecord): an event being logged.
            datefmt (str): ignored, RFC3339 format is always used.

        Returns:
            str: RFC3339 formatted timestamp
        """
        # Format with microseconds and Z suffix for UTC
        return datetime.fromtimestamp(record.created, tz=UTC).isoformat(timespec="microseconds").replace("+00:00", "Z")

    def format(self, record: logging.LogRecord) -> str:
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

        return logging.Formatter(log_fmt, self.datefmt).format(record)


class JSONFormatter(logging.Formatter):
    """Class used to serialize log messages in JSON and color them."""

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

    def formatTime(self, record: logging.LogRecord, datefmt=None):  # noqa: ARG002, N802
        """Format timestamp according to RFC3339 specification.

        Args:
            record (logging.LogRecord): an event being logged.
            datefmt (str): ignored, RFC3339 format is always used.

        Returns:
            str: RFC3339 formatted timestamp
        """
        # Format with microseconds and Z suffix for UTC
        return datetime.fromtimestamp(record.created, tz=UTC).isoformat(timespec="microseconds").replace("+00:00", "Z")

    def format(self, record: logging.LogRecord) -> str:
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


class ErrFilter(logging.Filter):
    """Class used to filter log messages based on level."""

    def filter(self, record: logging.LogRecord) -> bool:
        """Filter the log messages below WARNING level included.

        Args:
            record (logging.LogRecord): an event being logged.

        Returns:
            bool: if the record level is in or not.
        """
        return record.levelno in (logging.DEBUG, logging.INFO, logging.WARNING)


class Levels(Enum):
    """Class used to list log levels."""

    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


# Global
_log_instance = Log()


def set_log(log_instance: Log) -> None:
    """Set global instance.

    Args:
        log_instance (Log): log instance.
    """
    global _log_instance
    _log_instance = log_instance


def log() -> Log:
    """Get global instance.

    Returns:
        Log: log instance.
    """
    return _log_instance
