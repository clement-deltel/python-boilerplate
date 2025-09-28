#!/usr/bin/env python3
"""Module used to print log messages."""

# Standard Library
from logging import Handler, LogRecord


class PrintHandler(Handler):
    """Custom logging handler that prints log records."""

    def __init__(self) -> None:
        """Initialize class."""
        super().__init__()

    def emit(self, record: LogRecord) -> None:
        """Print a log record.

        Args:
            record (logging.LogRecord): log record to emit.
        """
        try:
            log_message = self.format(record)
            print(log_message, flush=True)

        except RecursionError:
            raise
        except Exception:
            self.handleError(record)

    def close(self) -> None:
        """Close the handler and cleanup resources."""
        super().close()
