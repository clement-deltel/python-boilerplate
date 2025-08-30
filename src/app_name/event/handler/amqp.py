#!/usr/bin/env python3
"""Module used to publish log messages to RabbitMQ."""

# Standard Library
from logging import Filter, Handler, LogRecord
from threading import Lock

# Local Application
from app_name.common.config import get_config_value
from app_name.event.publisher import AMQPPublisher


class AMQPLogHandler(Handler):
    """Custom logging handler that publishes log records to RabbitMQ.

    This handler integrates with the existing logging system and publishes
    log messages to RabbitMQ using the AMQPPublisher.
    """

    def __init__(self) -> None:
        """Initialize class."""
        super().__init__()
        self._lock = Lock()  # Add thread safety

        self._failed_messages = 0
        self._max_failed_messages = get_config_value("amqp", "max_failed_messages")

        self.amqp = AMQPPublisher()

    def emit(self, record: LogRecord) -> None:
        """Emit a log record to RabbitMQ.

        Args:
            record (logging.LogRecord): log record to emit.
        """
        try:
            with self._lock:
                # Skip if too many consecutive failed messages (circuit breaker pattern)
                if self._failed_messages >= self._max_failed_messages:
                    return

                log_message = self.format(record)
                if self.amqp.publish_message(log_message):
                    # Reset failed message counter on success
                    self._failed_messages = 0
                else:
                    self._failed_messages += 1

        except RecursionError:
            raise
        except Exception:
            self._failed_messages += 1
            self.handleError(record)

    def close(self) -> None:
        """Close the handler and cleanup resources."""
        self.amqp.close()
        super().close()


class AMQPFilter(Filter):
    """Class used to filter log messages based on module name."""

    def filter(self, record: LogRecord) -> bool:
        """Filter out log messages from the publisher module.

        Args:
            record (logging.LogRecord): log record to filter.

        Returns:
            bool: if the record is from the publisher module or not.
        """
        return record.module != "publisher"
