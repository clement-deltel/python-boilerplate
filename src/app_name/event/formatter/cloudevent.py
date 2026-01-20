"""Module providing a CloudEvent formatter for the logging system.

CloudEvents specification:
https://github.com/cloudevents/spec/blob/main/cloudevents/spec.md
"""

# Standard Library
import logging
from json import dumps
from typing import Any

# Third-party
from cloudevents.conversion import to_dict
from cloudevents.http import CloudEvent

# Local Application
from app_name.common.config import CloudEventsConfig, get_config_class
from app_name.event.formatter.colors import Colors


class CloudEventsFormatter(logging.Formatter):
    """Class used to serialize log messages in CloudEvents JSON format and color them."""

    def __init__(self, app_env: str, level: str, extra_fields: set, color_enabled: bool = False, pretty_json: bool = False) -> None:
        """Initialize class."""
        super().__init__()
        self.config: CloudEventsConfig = get_config_class("cloudevents")

        self.app_env = app_env
        self.level = level
        self.extra_fields = extra_fields
        self.color_enabled = color_enabled
        self.pretty_json = pretty_json

        self.colors = {item.name: item.value for item in Colors}
        self.reset = "\x1b[0m"

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as a CloudEvent.

        Args:
            record (logging.LogRecord): an event being logged.

        Returns:
            str: JSON-encoded CloudEvent.
        """
        info = record.__dict__.copy()

        # Required
        attributes: dict[str, Any] = {"specversion": self.config.spec_version, "type": self.config.type, "source": f"/{info['name']}/cloudevents"}

        # Optional
        attributes["subject"] = f"{record.module}::{record.funcName}:{record.lineno}"
        if "subject" in info:
            attributes["subject"] = info["subject"]

        # Data payload: contains message, and extra fields
        data: dict[str, Any] = {"message": record.getMessage()}

        # Add exception info if present
        if record.exc_info and record.exc_text is None:
            data["exc_info"] = self.formatException(record.exc_info)
        if record.stack_info:
            data["stack_info"] = self.formatStack(record.stack_info)
        # Handle extra
        for field in self.extra_fields:
            if field in info:
                data[field] = info[field]

        # Add more context in a debugging scenario
        if self.level == "DEBUG":
            data["module"] = record.module
            data["function"] = record.funcName
            data["lineno"] = record.lineno

        event = CloudEvent(attributes, data)
        # id: uuid randomly generated
        # time: timestamp automatically generated

        # Extension
        event["environment"] = self.app_env
        event["level"] = info["levelname"]

        # Optional - Data Content Type
        event["datacontenttype"] = self.config.data_content_type

        # Improve readability if requested
        pretty_options: dict[str, Any] = {}
        if self.pretty_json:
            pretty_options["indent"] = 2

        # Apply color if enabled
        if self.color_enabled:
            color = self.colors[record.levelname]
            log_message = color + dumps(to_dict(event), **pretty_options) + self.reset
        else:
            log_message = dumps(to_dict(event), **pretty_options)

        return log_message
