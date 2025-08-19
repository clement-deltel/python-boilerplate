#!/usr/bin/env python3
"""Main module of the application."""

# Standard Library
import sys
from os import environ
from platform import system
from re import sub
from signal import SIGINT, SIGQUIT, signal
from time import gmtime, perf_counter, strftime

# Local Application
from app_name.common.config import Config, DevConfig, ProdConfig, set_config
from app_name.common.profiler import profiler
from app_name.event.log import log


def signal_int_handler(signum, frame):
    """Handle SIGINT signal for the application execution."""
    log().logger.warning("You pressed Ctrl + C! Terminating gracefully...")
    raise KeyboardInterrupt


def signal_quit_handler(signum, frame):
    """Handle SIGQUIT signal for the application execution."""
    log().logger.warning("You pressed Ctrl + \\! Terminating gracefully...")
    raise KeyboardInterrupt


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


@profiler
def main() -> None:
    """Perform all the steps to run this application."""
    start = perf_counter()
    try:
        signal(SIGINT, signal_int_handler)
        if system() == "Linux":
            signal(SIGQUIT, signal_quit_handler)

        load_config()

    except KeyboardInterrupt:
        pass

    except Exception as err:
        log().logger.critical("A non-recoverable error occurred: %s. Aborting...", err)

    finally:
        # Print execution time
        end = perf_counter()
        exec_time = strftime("%H:%M:%S", gmtime(end - start))
        log().logger.info("Execution time: %s", exec_time)
        log().close()


if __name__ == "__main__":
    sys.argv[0] = sub(r"(-script\.pyw?|\.exe)?$", "", sys.argv[0])
    main()
    sys.exit()
