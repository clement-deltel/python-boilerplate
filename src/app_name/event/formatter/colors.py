"""Module used to list the colors for all the events of the application execution."""

# Standard Library
from enum import Enum


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
