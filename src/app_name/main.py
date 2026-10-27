#!/usr/bin/env python3
"""Main module of the Application Name."""

# Standard Library
import sys
from os import environ
from platform import system
from re import sub
from signal import SIGINT, signal
from time import gmtime, perf_counter, strftime
from types import FrameType

# Third-party
from dotenv import load_dotenv

# Local Application
from app_name.common.config import Config, DevConfig, ProdConfig, set_config
from app_name.common.debug import debug
from app_name.common.profiler import profiler
from app_name.event.logger.log import log

load_dotenv(".env", override=True)


def get_python_and_os() -> str:
    """Get both Python version and operating system.

    Returns:
        str: operating system.
    """
    # Python version & operating system
    operating_system = system()
    log().logger.debug("Python version: %s", sys.version)
    log().logger.debug("Operating system: %s", operating_system)

    return operating_system


def signal_int_handler(signum: int, frame: FrameType | None) -> None:  # noqa: ARG001
    """Handle SIGINT signal for the application execution.

    Raises:
        KeyboardInterrupt: user pressed Ctrl + C.
    """
    log().logger.warning("You pressed Ctrl + C! Terminating gracefully...")
    raise KeyboardInterrupt


def signal_quit_handler(signum: int, frame: FrameType | None) -> None:  # noqa: ARG001
    r"""Handle SIGQUIT signal for the application execution.

    Raises:
        KeyboardInterrupt: user pressed Ctrl + \\.
    """
    log().logger.warning("You pressed Ctrl + \\! Terminating gracefully...")
    raise KeyboardInterrupt


def set_signals(operating_system: str) -> None:
    """Initialize SIGINT and SIGQUIT.

    Args:
        operating_system (str): operating system name.
    """
    signal(SIGINT, signal_int_handler)

    if operating_system == "Linux":
        # Standard Library
        from signal import SIGQUIT  # noqa: PLC0415

        signal(SIGQUIT, signal_quit_handler)


def load_config() -> Config:
    """Load environment-based configuration.

    Returns:
        Config: config instance and all its attributes.
    """
    app_env = environ.get("APP_ENV", default="production")
    config_options = {"development": DevConfig, "production": ProdConfig}
    config: Config = config_options[app_env]()
    set_config(config)
    return config


@debug
@profiler
def main() -> None:
    """Perform all the steps to run this application."""
    start = perf_counter()
    try:
        operating_system = get_python_and_os()
        set_signals(operating_system)

        load_config()

    except KeyboardInterrupt:
        pass

    except Exception as err:
        log().logger.critical("A non-recoverable error occurred: %s. Aborting...", err)

    finally:
        # Print execution time
        end = perf_counter()
        log().logger.info("Execution time: %s", strftime("%H:%M:%S", gmtime(end - start)))
        log().close()


if __name__ == "__main__":
    sys.argv[0] = sub(r"(-script\.pyw?|\.exe)?$", "", sys.argv[0])
    main()
    sys.exit()
