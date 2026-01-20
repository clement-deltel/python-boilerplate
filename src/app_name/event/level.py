"""Module used to list and filter log levels."""

# Standard Library
from enum import Enum
from logging import CRITICAL, DEBUG, ERROR, INFO, WARNING, Filter, LogRecord


class Levels(Enum):
    """Class used to list log levels."""

    debug = DEBUG
    info = INFO
    warning = WARNING
    error = ERROR
    critical = CRITICAL


class ErrFilter(Filter):
    """Class used to filter log messages based on level."""

    def filter(self, record: LogRecord) -> bool:
        """Filter in log messages below WARNING level included.

        Args:
            record (logging.LogRecord): log record to filter.

        Returns:
            bool: if the record level is in or not.
        """
        return record.levelno in (DEBUG, INFO, WARNING)
