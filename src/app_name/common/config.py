#!/usr/bin/env python3
"""Module used to interact with the configuration."""

# Standard Library
from datetime import datetime
from os import environ
from typing import Any

# Third-party
from dotenv import load_dotenv

# Local Application
from app_name.common.path_translator import PathTranslator


def env_to_bool(variable: str) -> bool:
    """Ensure that environment variable is a boolean.

    Args:
        variable (str): environment variable string value.

    Returns:
        bool: environment variable boolean value.
    """
    return variable.casefold() in ("true", "t", "1")


def env_to_int(variable: str) -> int:
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

    def __init__(self, run_date: datetime, translator: PathTranslator) -> None:
        """Initialize class.

        Args:
            run_date (datetime): application run date.
            translator (PathTranslator): path translation between Windows and Linux formats.
        """
        self.app = AppConfig(run_date, translator)
        self.log = LogConfig(run_date, translator)

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

    def __init__(self, run_date: datetime, translator: PathTranslator) -> None:
        """Initialize class.

        Args:
            run_date (datetime): application run date.
            translator (PathTranslator): path translation between Windows and Linux formats.
        """
        self.name = "app-name"
        self.run_date = run_date

        # Directories and files
        self.input_path = translator.to_linux(environ.get("INPUT_PATH", default="input"))
        self.output_path = translator.to_linux(environ.get("OUTPUT_PATH", default="output"))
        self.output_path.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------- #
#               ------- Log Config ------
# ---------------------------------------------------------------------------- #
class LogConfig:
    """Class specifying attributes and methods related to the log configuration."""

    def __init__(self, run_date: datetime, translator: PathTranslator) -> None:
        """Initialize class.

        Args:
            run_date (datetime): application run date.
            translator (PathTranslator): path translation between Windows and Linux formats.
        """
        self.level = environ.get("LOG_LEVEL", default="INFO")
        self.path = translator.to_linux(environ.get("LOG_PATH", default="log"))
        self.file_path = self.path.joinpath(f"{run_date.strftime('%Y-%m-%d')}.log")
        self.to_file = env_to_bool(environ.get("LOG_TO_FILE", default="false"))
        # Log formatting
        self.color = env_to_bool(environ.get("LOG_COLOR", default="true"))
        self.json = env_to_bool(environ.get("LOG_JSON", default="true"))
        self.pretty = env_to_bool(environ.get("LOG_JSON_PRETTY", default="false"))

        if self.to_file:
            self.path.mkdir(parents=True, exist_ok=True)


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
        run_date = datetime.strptime(run_date_env, "%Y-%m-%d").astimezone() if run_date_env else datetime.now().astimezone()

        translator = PathTranslator(environ.get("MAPPINGS_PATH", default="C:\\:/mnt/"))

        super().__init__(run_date, translator)


# ---------------------------------------------------------------------------- #
#               ------- Production Config ------
# ---------------------------------------------------------------------------- #
class ProdConfig(Config):
    """Class specifying attributes and methods related to the production environment configuration."""

    def __init__(self) -> None:
        """Initialize class."""
        load_dotenv(".env", override=True)
        run_date = datetime.now().astimezone()

        translator = PathTranslator(environ.get("MAPPINGS_PATH", default="C:\\:/mnt/"))

        super().__init__(run_date, translator)


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
