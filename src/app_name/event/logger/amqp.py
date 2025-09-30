#!/usr/bin/env python3
"""Module used to log all the events of the related to the AMQP protocol."""

# Standard Library
from logging import StreamHandler, getLogger
from sys import stderr, stdout

# Local Application
from app_name.common.config import LogConfig, get_config_class
from app_name.event.formatter.cloudevent import CloudEventsFormatter
from app_name.event.formatter.custom import CustomFormatter
from app_name.event.formatter.json_f import JSONFormatter
from app_name.event.handler.print import PrintHandler
from app_name.event.level import ErrFilter, Levels


class AMQPLog:
    """Class specifying attributes and methods related to AMQP logging."""

    def __init__(self):
        """Initialize class."""
        self.config: LogConfig = get_config_class("log")
        self.levels = {item.name: item.value for item in Levels}

        self.extra_fields = {"amqp_host"}

        # Logger
        self._logger = getLogger("amqp_internal")
        # Formatters
        self.formatter = None
        # Handlers
        self.stream_handler_out = None
        self.stream_handler_err = None
        self.print_handler = None

        self.initialize()

    @property
    def logger(self):
        """Getter method for the attribute _logger."""
        return self._logger

    def initialize(self):
        """Initialize all logging components."""
        self.set_level(self.config.level)
        self.set_formatters(self.config.level)

        if self.config.print:
            self.open_print()
        else:
            self.open_stream()

    def set_level(self, level: str) -> None:
        """Set log level.

        Args:
            level (str): log level.
        """
        self._logger.setLevel(self.levels[level.lower()])

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
            self.stream_handler_out = StreamHandler(stream=stdout)
            self.stream_handler_out.setFormatter(self.formatter)
            self.stream_handler_out.setLevel(self.levels["debug"])
            self.stream_handler_out.addFilter(ErrFilter())
            self._logger.addHandler(self.stream_handler_out)
        if self.stream_handler_err is None:
            self.stream_handler_err = StreamHandler(stream=stderr)
            self.stream_handler_err.setFormatter(self.formatter)
            self.stream_handler_err.setLevel(self.levels["error"])
            self._logger.addHandler(self.stream_handler_err)

    def open_print(self) -> None:
        """Open the print handler to print log messages."""
        if self.print_handler is None:
            self.print_handler = PrintHandler()
            self.print_handler.setFormatter(self.formatter)
            self.print_handler.setLevel(self.levels["debug"])
            self._logger.addHandler(self.print_handler)

    def close(self) -> None:
        """Close stream, file, and amqp handlers."""
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


# Global
_amqp_log_instance = None


def set_log(log_instance: AMQPLog) -> None:
    """Set global instance.

    Args:
        log_instance (AMQPLog): log instance.
    """
    global _log_instance
    _log_instance = log_instance


def log() -> AMQPLog:
    """Get global instance.

    Returns:
        AMQPLog: log instance.
    """
    global _log_instance
    if _log_instance is None:
        _log_instance = AMQPLog()
    return _log_instance
