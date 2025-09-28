#!/usr/bin/env python3
"""Module used to debug the application."""

# Standard Library
from collections.abc import Callable
from functools import wraps
from os import environ

# Third-party
from debugpy import listen, wait_for_client
from dotenv import load_dotenv

# Local Application
from app_name.common.config import to_bool, to_int

load_dotenv(".env", override=True)


def debug(func: Callable):
    """Debug the target function."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        if to_bool(environ.get("DEBUGPY", default="false")):
            debug_host = environ.get("DEBUGPY_HOST", default="localhost")
            debug_port = to_int(environ.get("DEBUGPY_PORT", default="5678"))
            listen((debug_host, debug_port))

            if to_bool(environ.get("DEBUGPY_WAIT", default="true")):
                wait_for_client()

        return func(*args, **kwargs)

    return wrapper
