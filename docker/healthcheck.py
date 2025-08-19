#!/usr/bin/env python3
"""Application healthcheck script."""

# Standard Library
from os import environ
from subprocess import TimeoutExpired, run
from sys import exit as sys_exit


def is_process_running(pattern):
    """Check if a process matching the given pattern is running."""
    try:
        result = run(
            ["/usr/bin/pgrep", "-f", pattern],
            check=False,
            capture_output=True,
            timeout=5,  # Prevent hanging
        )
        return result.returncode == 0
    except (TimeoutExpired, FileNotFoundError) as err:
        print(f"Error checking process '{pattern}': {err}")
        return False


def get_expected_process(debug_entrypoint):
    """Get the expected process pattern based on current mode."""
    if debug_entrypoint:
        debug_command = environ.get("DEBUG_COMMAND", default="tail -f /dev/null")
        # Try full command first, fall back to first word
        return debug_command.strip(), debug_command.split()[0]
    pattern = "python -m src.app_name.main"
    return pattern, pattern


def main():
    """Main health check logic."""
    try:
        debug_entrypoint = environ.get("DEBUG_ENTRYPOINT", default="false").lower() in ("true", "t", "1")
        primary_pattern, fallback_pattern = get_expected_process(debug_entrypoint)
        mode = "DEBUG" if debug_entrypoint else "PRODUCTION"

        print(f"Health check running in {mode} mode")

        # Try primary pattern first
        if is_process_running(primary_pattern):
            print(f"Process found with pattern '{primary_pattern}' - Health check passed")
            sys_exit(0)

        # Try fallback pattern if different from primary
        if primary_pattern != fallback_pattern and is_process_running(fallback_pattern):
            print(f"Process found with fallback pattern '{fallback_pattern}' - Health check passed")
            sys_exit(0)

        print("No process found matching expected patterns - Health check failed")
        sys_exit(1)

    except Exception as e:
        print(f"Health check error: {e}")
        sys_exit(1)


if __name__ == "__main__":
    main()
