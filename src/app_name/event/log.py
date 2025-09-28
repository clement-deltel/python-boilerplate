#!/usr/bin/env python3
"""Module used to log all the events of the application execution.

Typical usage example:
  Log().open_stream()
  Log().set_level(args.log_level)
  Log().close_stream()
"""

# Standard Library
import logging
from enum import Enum
from sys import stderr, stdout

# Local Application
from app_name.common.config import LogConfig, get_config_class, get_config_value
from app_name.event.formatter.cloudevent import CloudEventsFormatter
from app_name.event.formatter.custom import CustomFormatter
from app_name.event.formatter.json_f import JSONFormatter
from app_name.event.handler.amqp import AMQPFilter, AMQPLogHandler
from app_name.event.handler.print import PrintHandler


class Log:
    """Class specifying attributes and methods related to logging."""

    def __init__(self):
        """Initialize class."""
        self.config: LogConfig = get_config_class("log")
        self.levels = {item.name: item.value for item in Levels}

        self.extra_fields = {"user_id", "table", "record", "wait"}

        # Logger
        self._logger = logging.getLogger(self.config.name)
        # Formatters
        self.formatter = None
        self.file_formatter = None
        # Handlers
        self.stream_handler_out = None
        self.stream_handler_err = None
        self.print_handler = None
        self.file_handler = None
        self.amqp_handler = None

        self.initialize()

    @property
    def logger(self):
        """Getter method for the attribute _logger."""
        return self._logger

    def initialize(self):
        """."""
        self.set_level(self.config.level)
        self.set_formatters(self.config.level)

        if get_config_value("debug", "print"):
            self.open_print()
        else:
            self.open_stream()

        if self.config.to_file:
            self.open_file(str(self.config.file_path))
        if self.config.to_amqp:
            self.open_amqp()

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
        self.formatter = CustomFormatter(self.config.app_env, level, self.extra_fields, self.config.color)
        # JSON formatter
        if self.config.json:
            self.formatter = JSONFormatter(self.config.app_env, level, self.extra_fields, self.config.color, self.config.pretty)
        # CloudEvents formatter
        if self.config.cloudevents:
            self.formatter = CloudEventsFormatter(self.config.app_env, level, self.extra_fields, self.config.color, self.config.pretty)

    def open_stream(self) -> None:
        """Open the stream handlers to write log messages to stdout and stderr."""
        if self.stream_handler_out is None:
            self.stream_handler_out = logging.StreamHandler(stream=stdout)
            self.stream_handler_out.setFormatter(self.formatter)
            self.stream_handler_out.setLevel(self.levels["DEBUG"])
            self.stream_handler_out.addFilter(ErrFilter())
            self._logger.addHandler(self.stream_handler_out)
        if self.stream_handler_err is None:
            self.stream_handler_err = logging.StreamHandler(stream=stderr)
            self.stream_handler_err.setFormatter(self.formatter)
            self.stream_handler_err.setLevel(self.levels["ERROR"])
            self._logger.addHandler(self.stream_handler_err)

    def open_print(self) -> None:
        """Open the print handler to print log messages."""
        if self.print_handler is None:
            self.print_handler = PrintHandler()
            self.print_handler.setFormatter(self.formatter)
            self.print_handler.setLevel(self.levels["DEBUG"])
            self._logger.addHandler(self.print_handler)

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

    def open_amqp(self) -> None:
        """Open the AMQP handler to write log messages to RabbitMQ."""
        if self.amqp_handler is None:
            self.amqp_handler = AMQPLogHandler()
            self.amqp_handler.setFormatter(self.formatter)
            self.amqp_handler.setLevel(self.levels["DEBUG"])
            self.amqp_handler.addFilter(AMQPFilter())
            self._logger.addHandler(self.amqp_handler)

    def close(self) -> None:
        """Close stream, file, and amqp handlers."""
        self.close_amqp()
        self.close_file()
        self.close_print()
        self.close_stream()

    def close_stream(self) -> None:
        """Close the stream handlers."""
        if self.stream_handler_out is not None:
            try:
                self._logger.removeHandler(self.stream_handler_out)
                self.stream_handler_out.close()
            except Exception as err:
                self._logger.warning("Error closing stdout stream handler: %s", err)
            finally:
                self.stream_handler_out = None

        if self.stream_handler_err is not None:
            try:
                self._logger.removeHandler(self.stream_handler_err)
                self.stream_handler_err.close()
            except Exception as err:
                self._logger.warning("Error closing stderr stream handler: %s", err)
            finally:
                self.stream_handler_err = None

    def close_print(self) -> None:
        """Close the print handler."""
        if self.print_handler is not None:
            try:
                self._logger.removeHandler(self.print_handler)
                self.print_handler.close()
            except Exception as err:
                self._logger.warning("Error closing print handler: %s", err)
            finally:
                self.print_handler = None

    def close_file(self) -> None:
        """Close the file handler."""
        if self.file_handler is not None:
            try:
                self._logger.removeHandler(self.file_handler)
                self.file_handler.close()
            except Exception as err:
                self._logger.warning("Error closing file handler: %s", err)
            finally:
                self.file_handler = None

    def close_amqp(self) -> None:
        """Close the AMQP handler."""
        if self.amqp_handler is not None:
            try:
                self._logger.removeHandler(self.amqp_handler)
                self.amqp_handler.close()
            except Exception as err:
                # Log the error but don't raise to avoid issues during shutdown
                self._logger.warning("Error closing AMQP handler: %s", err)
            finally:
                self.amqp_handler = None


class ErrFilter(logging.Filter):
    """Class used to filter log messages based on level."""

    def filter(self, record: logging.LogRecord) -> bool:
        """Filter in log messages below WARNING level included.

        Args:
            record (logging.LogRecord): log record to filter.

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
_log_instance = None


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
    global _log_instance
    if _log_instance is None:
        _log_instance = Log()
    return _log_instance
