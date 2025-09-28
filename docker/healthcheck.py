#!/usr/bin/env python3
"""Application healthcheck script."""

# Standard Library
from os import environ
from pathlib import Path
from sys import exit as sys_exit


def is_process_running(pattern):
    """Check if a process matching the given pattern is running using /proc."""
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


def main():
    """Main health check logic."""
    try:
        debug = environ.get("DEBUG", default="false").lower() in ("true", "t", "1")
        mode = "DEBUG" if debug else "PRODUCTION"
        pattern = "app_name"

        print(f"Health check running in {mode} mode")

        # Try primary pattern first
        if is_process_running(pattern):
            print(f"Process found with pattern '{pattern}' - Health check passed")
            sys_exit(0)

        print("No process found matching expected patterns - Health check failed")
        sys_exit(1)

    except Exception as e:
        print(f"Health check error: {e}")
        sys_exit(1)


if __name__ == "__main__":
    main()
