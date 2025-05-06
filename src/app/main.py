#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Main module of the RAN Replicator Service."""

# Standard imports
import signal
import sys
import time
from functools import wraps
from os import environ
from re import sub

# Third-party imports
from dotenv import load_dotenv

# Local application imports
from src.app.common.config import Config, DevConfig, ProdConfig, set_config
from src.app.common.log import log
from src.app.common.profiler import Profiler


class Main:
    """Main class containing the method for running the RAN Replicator Service."""

    @staticmethod
    def signal_quit_handler(signum, frame) -> None:
        """Handle SIGQUIT signal for the application execution."""
        log().logger.warning("You pressed Ctrl + \\! Terminating gracefully...")
        raise KeyboardInterrupt

    @staticmethod
    def signal_int_handler(signum, frame) -> None:
        """Handle SIGINT signal for the application execution."""
        log().logger.warning("You pressed Ctrl + C! Terminating gracefully...")
        raise KeyboardInterrupt

    def run(self) -> None:
        """Perform all the steps to run this application."""
        start = time.perf_counter()
        try:
            # Normal if there is an error in Windows, SIGQUIT exists only in Unix
            signal.signal(signal.SIGQUIT, self.signal_quit_handler)
            signal.signal(signal.SIGINT, self.signal_int_handler)

            # Load environment-based configuration
            app_env = environ.get("APP_ENV", default="production")
            config_options = {"development": DevConfig, "production": ProdConfig}
            cfg: Config = config_options[app_env]()
            set_config(cfg)

        except KeyboardInterrupt:
            pass

        except Exception as err:
            log().logger.critical("A non-recoverable error occurred: %s. Aborting...", err)

        finally:
            # Print execution time
            end = time.perf_counter()
            exec_time = time.strftime("%H:%M:%S", time.gmtime(end - start))
            log().logger.info("Execution time: %s", exec_time)
            log().close()


def profile_if_enabled(func):
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


@profile_if_enabled
def main():
    """Run the application."""
    Main().run()


if __name__ == "__main__":
    sys.argv[0] = sub(r"(-script\.pyw?|\.exe)?$", "", sys.argv[0])
    load_dotenv(".env", override=True)
    main()
    sys.exit()
