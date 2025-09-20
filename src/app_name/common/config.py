#!/usr/bin/env python3
"""Module used to interact with the configuration."""

# Standard Library
from datetime import UTC, datetime
from os import environ
from typing import Any

# Third-party
from dotenv import load_dotenv

# Local Application
from app_name.common.path_translator import to_path


def to_bool(variable: str) -> bool:
    """Ensure that environment variable is a boolean.

    Args:
        variable (str): environment variable string value.

    Returns:
        bool: environment variable boolean value.
    """
    return variable.casefold() in ("true", "t", "1")


def to_int(variable: str) -> int:
    """Ensure that environment variable is a integer.

    Args:
        variable (str): environment variable string value.

    Returns:
        int: environment variable integer value.
    """
    try:
        return int(variable)
    except ValueError as err:
        print(f"ValueError: {variable} cast to int failed")
        raise Exception from err


# ---------------------------------------------------------------------------- #
#               ------- Config ------
# ---------------------------------------------------------------------------- #
class Config:
    """Class specifying attributes and methods related to the configuration."""

    def __init__(self, app_env: str, run_date: datetime) -> None:
        """Initialize class.

        Args:
            app_env (str): application environment.
            run_date (datetime): application run date.
        """
        name = "app-name"

        # Logging
        self.amqp = AMQPConfig()
        self.cloudevents = CloudEventsConfig()
        self.log = LogConfig(name, app_env, run_date)

        # Application
        self.app = AppConfig(name, run_date)

    def get_config_class(self, class_name: str, default: Any) -> Any:
        """Get class.

        Args:
            class_name (str): class name.
            default (Any): value to return if class instance not found.

        Returns:
            Any: configuration instance.
        """
        return getattr(self, class_name, default)

    def get_config_value(self, class_name: str, attribute: str, default: Any) -> Any:
        """Get attribute.

        Args:
            class_name (str): class name.
            attribute (str): attribute name.
            default (Any): value to return if attribute not found.

        Returns:
            Any: configuration attribute.
        """
        config_class = getattr(self, class_name, None)
        if config_class is None:
            raise ValueError(f"Config class '{class_name}' not found")

        return getattr(config_class, attribute, default)


# ---------------------------------------------------------------------------- #
#               ------- Application Config ------
# ---------------------------------------------------------------------------- #
class AppConfig:
    """Class specifying attributes and methods related to the application configuration."""

    def __init__(self, name: str, run_date: datetime) -> None:
        """Initialize class.

        Args:
            name (str): application name.
            run_date (datetime): application run date.
            translator (PathTranslator): path translation between Windows and Linux formats.
        """
        self.name = name
        self.run_date = run_date

        # Directories and files
        self.input_path = to_path(environ.get("INPUT_PATH", default="/app/input"))
        self.output_path = to_path(environ.get("OUTPUT_PATH", default="/app/output"))
        self.output_path.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------- #
#               ------- Log Config ------
# ---------------------------------------------------------------------------- #
class LogConfig:
    """Class specifying attributes and methods related to the log configuration."""

    def __init__(self, name: str, app_env: str, run_date: datetime) -> None:
        """Initialize class.

        Args:
            name (str): application name.
            app_env (str): application environment.
            run_date (datetime): application run date.
            translator (PathTranslator): path translation between Windows and Linux formats.
        """
        self.name = name
        self.app_env = app_env

        self.level = environ.get("LOG_LEVEL", default="INFO")

        # Log handlers
        self.path = to_path(environ.get("LOG_PATH", default="log"))
        self.file_path = self.path.joinpath(f"{run_date.strftime('%Y-%m-%dT%H%M%S')}.log")
        self.to_file = to_bool(environ.get("LOG_TO_FILE", default="false"))
        self.to_amqp = to_bool(environ.get("LOG_TO_AMQP", default="false"))

        # Log formatting
        self.cloudevents = to_bool(environ.get("LOG_CLOUDEVENTS", default="true"))
        self.color = to_bool(environ.get("LOG_COLOR", default="true"))
        self.json = to_bool(environ.get("LOG_JSON", default="false"))
        self.pretty = to_bool(environ.get("LOG_JSON_PRETTY", default="false"))

        if self.to_file:
            self.path.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------- #
#               ------- AMQP Config ------
# ---------------------------------------------------------------------------- #
class AMQPConfig:
    """Class specifying attributes and methods related to the AMQP protocol."""

    def __init__(self) -> None:
        """Initialize class."""
        # Required
        self.hostname = environ.get("AMQP_HOSTNAME", default="localhost")
        self.port = to_int(environ.get("AMQP_PORT", default="5672"))
        self.username = environ.get("AMQP_USERNAME", default="guest")
        self.password = environ.get("AMQP_PASSWORD", default="guest")

        self.exchange = environ.get("AMQP_EXCHANGE", default="")
        self.exchange_type = environ.get("AMQP_EXCHANGE_TYPE", default="topic")
        self.routing_key = environ.get("AMQP_ROUTING_KEY", default="#")

        # Connection settings
        self.virtual_host = environ.get("AMQP_VIRTUAL_HOST", default="/")

        # Connection reliability
        self.heartbeat = to_int(environ.get("AMQP_HEARTBEAT", default="600"))
        self.connection_attempts = to_int(environ.get("AMQP_CONNECTION_ATTEMPTS", default="3"))
        self.retry_delay = to_int(environ.get("AMQP_RETRY_DELAY", default="2"))
        self.socket_timeout = to_int(environ.get("AMQP_SOCKET_TIMEOUT", default="10"))
        self.blocked_connection_timeout = to_int(environ.get("AMQP_BLOCKED_CONNECTION_TIMEOUT", default="300"))

        # Publishing
        self.exchange_durable = to_bool(environ.get("AMQP_EXCHANGE_DURABLE", default="true"))
        self.message_persistent = to_bool(environ.get("AMQP_MESSAGE_PERSISTENT", default="true"))

        # Circuit breaker pattern
        self.max_failed_messages = to_int(environ.get("AMQP_MAX_FAILED_MESSAGES", default="10"))


# ---------------------------------------------------------------------------- #
#               ------- CloudEvents Config ------
# ---------------------------------------------------------------------------- #
class CloudEventsConfig:
    """Class specifying attributes and methods related to the CloudEvents specification."""

    def __init__(self) -> None:
        """Initialize class."""
        # Required
        self.spec_version = environ.get("CLOUDEVENTS_SPEC_VERSION", default="1.0")
        self.type = environ.get("CLOUDEVENTS_TYPE", default="com.customer.app_name.v1")

        # Optional
        self.data_content_type = environ.get("CLOUDEVENTS_DATA_CONTENT_TYPE", default="application/json")


# ---------------------------------------------------------------------------- #
#               ------- Development Config ------
# ---------------------------------------------------------------------------- #
class DevConfig(Config):
    """Class specifying attributes and methods related to the development environment configuration."""

    def __init__(self) -> None:
        """Initialize class."""
        load_dotenv(".env", override=True)
        # Custom date specifically to tweak run date and trigger certain behaviors
        run_date_env = environ.get("RUN_DATE", default="")
        run_date = datetime.strptime(run_date_env, "%Y-%m-%d").astimezone(UTC) if run_date_env else datetime.now(UTC)

        super().__init__("development", run_date)


# ---------------------------------------------------------------------------- #
#               ------- Production Config ------
# ---------------------------------------------------------------------------- #
class ProdConfig(Config):
    """Class specifying attributes and methods related to the production environment configuration."""

    def __init__(self) -> None:
        """Initialize class."""
        load_dotenv(".env", override=True)
        run_date = datetime.now(UTC)

        super().__init__("production", run_date)


# Global
_config_instance = None


def set_config(config: Config) -> None:
    """Set global instance.

    Args:
        config (Config): configuration instance.
    """
    global _config_instance
    _config_instance = config


def get_config() -> Config:
    """Get global instance.

    Returns:
        Config: config instance, whether ProdConfig or DevConfig.
    """
    global _config_instance
    if _config_instance is None:
        _config_instance = ProdConfig()
    return _config_instance


def get_config_class(class_name: str, default: Any = None) -> Any:
    """Get class.

    Args:
        class_name (str): class name.
        default (Any, optional): value to return if class instance not found. Defaults to None.

    Returns:
        Any: configuration class instance.
    """
    return get_config().get_config_class(class_name, default)


def get_config_value(class_name: str, attribute: str, default: Any = None) -> Any:
    """Get attribute.

    Args:
        class_name (str): class name.
        attribute (str): attribute name.
        default (Any, optional): value to return if attribute not found. Defaults to None.

    Returns:
        Any: configuration class attribute.
    """
    return get_config().get_config_value(class_name, attribute, default)
