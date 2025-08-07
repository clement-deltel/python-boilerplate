#!/usr/bin/env python3
"""Pre-commit hook to update README.md with fresh tokei code statistics."""

# Standard Library
import sys
from argparse import ArgumentParser, Namespace
from pathlib import Path
from re import DOTALL, search, sub
from subprocess import CalledProcessError, run


def parse_args() -> Namespace:
    """Parse command-line options.

    Returns:
        argparse.Namespace: populated with user input arguments.
    """
    parser = ArgumentParser(description="Update README.md sections with command output", add_help=False)

    # Argument groups
    required = parser.add_argument_group("Required arguments")
    optional = parser.add_argument_group("Optional arguments")
    others = parser.add_argument_group("Help")

    # Required arguments
    required.add_argument(
        "-c", "--command", action="store", default=None, help="Command to run to get the output for README update", metavar="COMMAND", required=True, type=str
    )

    required.add_argument(
        "-e",
        "--regex",
        action="store",
        default=None,
        help="Regular expression to identify README section (must have 3 capture groups)",
        metavar="PATTERN",
        required=True,
        type=str,
    )

    # Optional arguments
    optional.add_argument("--dry-run", action="store_true", help="Show what would be updated without making changes")

    # Other arguments
    others.add_argument("-h", "--help", action="help", help="show this help message and exit")

    # Do the parsing
    if len(sys.argv) == 1:
        parser.print_help(sys.stdout)
        sys.exit(0)
    return parser.parse_args()


def run_command(command: str) -> str | None:
    """Run command and return stdout output.

    Args:
        command (str): shell command to execute.

    Returns:
        str | None: command output.
    """
    command_parts = command.split(" ")
    name = command_parts[0]
    try:
        result = run(command_parts, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except CalledProcessError as err:
        print(f"Error running {name} command: {err}")
        print(f"Make sure {name} is installed and available in PATH")
        return None
    except FileNotFoundError:
        print(f"Error: {name} command not found. Please install {name} first.")
        return None


def get_readme() -> Path | None:
    """Get README.md file absolute path in the current directory or parent directories.

    Returns:
        Path | None: README file absolute path.
    """
    current_dir = Path.cwd()

    # Check current directory and all parents
    for directory in [current_dir, *list(current_dir.parents)]:
        if directory.joinpath("README.md").is_file():
            return directory.joinpath("README.md")

    return None


def update_readme(path: Path, pattern: str, command_output: str) -> bool:
    """Update README section with command output.

    Args:
        path (Path): README file absolute path.
        pattern (str): regular expression to identify the text block to be updated.
        command_output (str): up-to-date command output.

    Returns:
        bool: is README update successful or not.
    """
    # Read README.md file
    try:
        content = path.read_text(encoding="utf-8")
    except Exception as err:
        print(f"Error reading README.md: {err}")
        return False

    # Check if the pattern exists
    if not search(pattern, content, DOTALL):
        print("Error: Pattern not found in README.md")
        print("Ensure your regex has exactly 3 capture groups: (prefix)(content)(suffix)")
        return False

    # Replace the content between the code blocks
    new_content = sub(pattern, rf"\1{command_output}\3", content, flags=DOTALL)

    # Write the updated content back
    try:
        path.write_text(new_content, encoding="utf-8")
        print("✓ README.md updated successfully")
        return True
    except Exception as err:
        print(f"Error writing to README.md: {err}")
        return False


def main() -> int:
    """Main function to run the pre-commit hook.

    Returns:
        int: pre-commit hook return code.
    """
    print("Running README update pre-commit hook...")
    args = parse_args()

    # Get README.md
    path = get_readme()
    if not path:
        print("Error: README.md not found in current directory or parent directories")
        return 1
    print("✓ README.md found")

    # Run command
    command_output = run_command(args.command)
    if not command_output:
        return 1

    # Update README.md
    if not update_readme(path, args.regex, command_output):
        return 1

    # Diff/Stage the updated README.md for commit
    try:
        if args.dry_run:
            ps = run(["/usr/bin/git", "diff", str(path)], check=True, capture_output=True)
            print(ps.stdout.decode("utf-8"))
        else:
            run(["/usr/bin/git", "add", str(path)], check=True, capture_output=True)
            print("✓ README.md staged for commit")
    except CalledProcessError as err:
        print(f"Warning: Could not stage README.md: {err}")
        print("You may need to manually stage the file")

    print("✓ Pre-commit hook completed successfully")
    return 0


if __name__ == "__main__":
    sys.exit(main())
