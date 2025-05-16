#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Main module of the RAN Replicator Service."""

# Standard imports
import sys
from functools import wraps
from os import environ
from platform import system
from re import sub
from signal import SIGINT, SIGQUIT, signal
from time import gmtime, perf_counter, strftime
from typing import Callable

# Third-party imports
from dotenv import load_dotenv

# Local application imports
from src.app.common.config import Config, DevConfig, ProdConfig, set_config
from src.app.common.log import log
from src.app.common.profiler import Profiler


class Main:
    """Main class containing the method for running the RAN Replicator Service."""

    @staticmethod
    def signal_int_handler(signum, frame):
        """Handle SIGINT signal for the application execution."""
        log().logger.warning("You pressed Ctrl + C! Terminating gracefully...")
        raise KeyboardInterrupt

    @staticmethod
    def signal_quit_handler(signum, frame):
        """Handle SIGQUIT signal for the application execution."""
        log().logger.warning("You pressed Ctrl + \\! Terminating gracefully...")
        raise KeyboardInterrupt

    def run(self) -> None:
        """Perform all the steps to run this application."""
        start = perf_counter()
        try:
            signal(SIGINT, self.signal_int_handler)
            if system() == "Linux":
                signal(SIGQUIT, self.signal_quit_handler)

            # Load environment-based configuration
            app_env = environ.get("APP_ENV", default="production")
            config_options = {"development": DevConfig, "production": ProdConfig}
            config: Config = config_options[app_env]()
            set_config(config)

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


def profiler(func: Callable):
    """Enable profiling on the target function."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        profiling = environ.get("PROFILING", "false").lower() in ("true", "t", "1")
        if profiling:
            profiler = Profiler()
            profiler.start()
            result = func(*args, **kwargs)
            profiler.end()
            return result
        return func(*args, **kwargs)

    return wrapper


@profiler
def main():
    """Run the application."""
    Main().run()


if __name__ == "__main__":
    sys.argv[0] = sub(r"(-script\.pyw?|\.exe)?$", "", sys.argv[0])
    load_dotenv(".env", override=True)
    main()
    sys.exit()
