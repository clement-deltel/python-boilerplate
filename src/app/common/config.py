#!/usr/bin/env python3
"""Module used to interact with the configuration."""

# Standard Library
from datetime import datetime
from os import environ
from pathlib import Path
from typing import Any

# Third-party
from dotenv import load_dotenv


class Config:
    """Class specifying attributes and methods related to the configuration."""

    def __init__(self, run_date: datetime) -> None:
        """Initialize class.

        Args:
            run_date (datetime): application run date.
        """
        self.app = AppConfig(run_date)
        self.log = LogConfig(run_date)

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


class AppConfig:
    """Class specifying attributes and methods related to the application configuration."""

    def __init__(self, run_date: datetime) -> None:
        """Initialize class.

        Args:
            run_date (datetime): application run date.
        """
        self.name = "app"
        self.run_date = run_date

        # Directories and files
        self.input_path = Path(environ.get("INPUT_PATH", default="input"))
        self.output_path = Path(environ.get("OUTPUT_PATH", default="output"))
        self.output_path.mkdir(parents=True, exist_ok=True)


class LogConfig:
    """Class specifying attributes and methods related to the log configuration."""

    def __init__(self, run_date: datetime) -> None:
        """Initialize class.

        Args:
            run_date (datetime): application run date.
        """
        self.level = environ.get("LOG_LEVEL", default="INFO")
        self.path = Path(environ.get("LOG_PATH", default="log"))
        self.file_path = Path.joinpath(self.path, f"{run_date.strftime('%Y-%m-%d')}.log")
        self.to_file = environ.get("LOG_TO_FILE", default="false").lower() in ("true", "t", "1")
        # Log formatting
        self.color = environ.get("LOG_COLOR", default="true").lower() in ("true", "t", "1")
        self.json = environ.get("LOG_JSON", default="true").lower() in ("true", "t", "1")
        self.pretty = environ.get("LOG_JSON_PRETTY", default="false").lower() in ("true", "t", "1")

        if self.to_file:
            self.path.mkdir(parents=True, exist_ok=True)


class DevConfig(Config):
    """Class specifying attributes and methods related to the development environment configuration."""

    def __init__(self) -> None:
        """Initialize class."""
        load_dotenv(".env", override=True)
        # Custom date specifically to tweak run date and trigger certain behaviors
        run_date_env = environ.get("RUN_DATE", default="")
        run_date = datetime.strptime(run_date_env, "%Y-%m-%d").astimezone() if run_date_env else datetime.now().astimezone()

        super().__init__(run_date)


class ProdConfig(Config):
    """Class specifying attributes and methods related to the production environment configuration."""

    def __init__(self) -> None:
        """Initialize class."""
        load_dotenv(".env", override=True)
        run_date = datetime.now().astimezone()
        super().__init__(run_date)


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
    config = get_config()
    return config.get_config_class(class_name, default)


def get_config_value(class_name: str, attribute: str, default: Any = None) -> Any:
    """Get attribute.

    Args:
        class_name (str): class name.
        attribute (str): attribute name.
        default (Any, optional): value to return if attribute not found. Defaults to None.

    Returns:
        Any: configuration class attribute.
    """
    config = get_config()
    return config.get_config_value(class_name, attribute, default)
