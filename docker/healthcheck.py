#!/usr/bin/env python3
"""Application healthcheck script."""

# Standard Library
from os import environ
from pathlib import Path
from sys import exit as sys_exit

# Global variables
PROCESS = "app_name"


def is_process_running(pattern: str) -> bool:
    """Check if a process matching the given pattern is running using /proc.

    Args:
        pattern(str): process name.

    Returns:
        bool: process found running or not.
    """
    try:
        proc_dir = Path("/proc")
        for pid_dir in proc_dir.iterdir():
            if not pid_dir.name.isdigit():
                continue

            try:
                # Read the command line of the process
                cmdline_file = pid_dir / "cmdline"
                with cmdline_file.open("r") as f:
                    cmdline = f.read().replace("\0", " ").strip()

                if pattern in cmdline:
                    return True

            except (OSError, PermissionError):
                # Process might have disappeared or we don't have permission
                continue

        return False

    except OSError as err:
        print(f"Error checking process '{pattern}': {err}")
        return False


def main() -> None:
    """Run health check."""
    try:
        debug = environ.get("DEBUG", default="false").lower() in ("true", "t", "1")
        mode = "DEBUG" if debug else "PRODUCTION"
        print(f"Health check running in {mode} mode")

        # Try primary pattern first
        if is_process_running(PROCESS):
            print(f"Process '{PROCESS}' found - Health check passed")
            sys_exit(0)

        print(f"Process '{PROCESS}' not found - Health check failed")
        sys_exit(1)

    except Exception as e:
        print(f"Health check error: {e}")
        sys_exit(1)


if __name__ == "__main__":
    main()
