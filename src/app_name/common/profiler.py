#!/usr/bin/env python3
"""Module used to run the profiler."""

# Standard Library
from cProfile import Profile
from collections.abc import Callable
from functools import wraps
from os import environ
from pathlib import Path
from pstats import Stats

# Third-party
from dotenv import load_dotenv

# Local Application
from app_name.common.config import get_config_value, to_bool


class Profiler:
    """Class specifying attributes and methods related to the profiler."""

    def __init__(self) -> None:
        """Initialize class."""
        self.profiler = Profile()

    def start(self) -> None:
        """Start profiler."""
        self.profiler.enable()

    def end(self) -> None:
        """Terminate profiler, format and export results."""
        self.profiler.disable()

        # Get and format results
        stats = Stats(self.profiler).strip_dirs().sort_stats("cumtime")

        # Export results
        output_path = get_config_value("app", "output_path")
        name = get_config_value("app", "name")
        run_date = get_config_value("app", "run_date")
        export_file_path = Path.joinpath(output_path, f"{run_date.strftime('%Y-%m-%dT%H%M%S')}_{name}.prof")
        stats.dump_stats(export_file_path)


def profiler(func: Callable):
    """Enable profiling on the target function."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        load_dotenv(".env", override=True)

        if to_bool(environ.get("PROFILING", default="false")):
            profiler = Profiler()
            profiler.start()
            result = func(*args, **kwargs)
            profiler.end()
            return result
        return func(*args, **kwargs)

    return wrapper
