#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Module used to log all the events of the application execution.

Typical usage example:
  Log().open_stream()
  Log().set_level(args.log_level)
  Log().close_stream()
"""

# Standard
import logging
from enum import Enum
from json import dumps
from sys import stderr, stdout
from typing import Any

# Local application
from app.common.config import get_config_class, get_config_value


class Log:
    """Class specifying attributes and methods related to logging."""

    def __init__(self):
        """Initialize class."""
        self.config = get_config_class("log")
        self.levels = {item.name: item.value for item in Levels}

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
        if self.config.to_file:
            self.open()
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
        self.file_formatter = CustomFormatter(level, datefmt="%d-%b-%Y %H:%M:%S")
        self.stream_formatter = CustomFormatter(level, self.config.color)
        # JSON formatters
        if self.config.json:
            self.stream_formatter = JSONFormatter(level, self.config.color, self.config.pretty)

    def open(self) -> None:
        """Open both stream and file handlers."""
        self.open_stream()
        self.open_file(str(self.config.file_path))

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

    def __init__(self, level: str, color_enabled: bool = False, datefmt: str = ""):
        """Initialize class."""
        super().__init__()
        self.level = level
        self.color_enabled = color_enabled
        self.datefmt = datefmt

        self.colors = {item.name: item.value for item in Colors}
        self.fmt = "%(asctime)-20s - %(levelname)-8s - %(message)s"
        self.reset = "\x1b[0m"

    def format(self, record: logging.LogRecord) -> str:
        """Retrieve extra information and apply different colors to the log messages.

        Args:
            record (logging.LogRecord): an event being logged.

        Returns:
            str: record formatted as text.

        """
        # info = record.__dict__.copy()
        message = self.fmt.split("%")
        # Handle extra
        # if "record" in info:
        #     message[-1] += " - "
        #     message.append("(record)s")
        fmt = "%".join(message)
        # Add more context in a debugging scenario
        if self.level == "DEBUG":
            fmt = fmt + " (%(module)s:%(lineno)s)"

        # Apply color if enabled
        if self.color_enabled:
            color = self.colors[record.levelname]
            log_fmt = color + fmt + self.reset
        else:
            log_fmt = fmt

        formatter = logging.Formatter(log_fmt, self.datefmt)
        return formatter.format(record)


class JSONFormatter(logging.Formatter):
    """Class used to serialize log messages in JSON and color them."""

    def __init__(self, level: str, color_enabled: bool = False, pretty_json: bool = False) -> None:
        """Initialize class."""
        super().__init__()
        self.level = level
        self.color_enabled = color_enabled
        self.pretty_json = pretty_json
        self.colors = {item.name: item.value for item in Colors}
        self.reset = "\x1b[0m"

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
        # if "record" in info:
        #     message["record"] = info["record"]
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


class Colors(Enum):
    """Class used to list log colors."""

    # Blue
    DEBUG = "\x1b[34m"
    # White
    INFO = "\x1b[39m"
    # Yellow
    WARNING = "\x1b[33m"
    # Light red
    ERROR = "\x1b[91m"
    # Red
    CRITICAL = "\x1b[31m"


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
