#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Module used to run the profiler."""

# Standard imports
from cProfile import Profile
from pathlib import Path
from pstats import Stats

# Local application imports
from src.app.common.config import get_config_value


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
        stats = Stats(self.profiler)

        # Format results
        stats = stats.strip_dirs()
        stats = stats.sort_stats("cumtime")

        # Export results
        output_path = get_config_value("app", "output_path")
        name = get_config_value("app", "name")
        run_date = get_config_value("app", "run_date")
        export_file_path = Path.joinpath(output_path, f"{run_date.strftime('%Y%m%d')}_{name}.prof")
        stats.dump_stats(export_file_path)
