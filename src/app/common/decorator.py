#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Decorators used across the application."""

# Standard imports
from functools import wraps
from os import environ

# Local application imports
from src.app.common.profiler import Profiler


def profiler(func):
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
