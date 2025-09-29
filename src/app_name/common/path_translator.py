#!/usr/bin/env python3
"""Module used to map paths between Linux and Windows systems.

This module provides utilities for translating paths between Linux and Windows formats using configurable path mappings. It handles cross-platform path
conversion while maintaining proper path semantics.
"""

# Standard Library
from os import environ
from pathlib import Path, PurePosixPath, PureWindowsPath
from platform import system

# Third-party
from dotenv import load_dotenv

load_dotenv(".env", override=True)


class PathMappingError(Exception):
    """Custom exception for path mapping errors."""

    pass


class PathTranslationError(Exception):
    """Custom exception for path translation errors."""

    pass


class PathTranslator:
    """A class to handle cross-platform path mapping and translation.

    This class encapsulates path mapping logic based on an environment variable and provides methods for bidirectional path translation with proper
    validation and error handling.
    """

    def __init__(self, mappings_env: str = "") -> None:
        """Initialize the class."""
        self._valid_targets = {"auto", "linux", "windows"}

        # Detect current operating system
        operating_system = system()
        self._system = "linux" if operating_system in ("Linux", "Darwin") else "windows"

        # Parse mappings from environment variable
        self._mappings = self._parse_mappings(mappings_env)

    def _parse_mappings(self, mappings_env: str) -> dict[str, dict[str, str]]:
        """Parse path mappings.

        Args:
            mappings_env (str): mappings environment variable.

        Returns:
            dict[str, dict[str,str]]: dictionary mapping source paths to destination paths, divided by category.

        Raises:
            PathMappingError: if mappings format is invalid.
        """
        mappings = {"cross-platform": {}, "linux": {}, "windows": {}}
        pair_length = 2

        if not mappings_env.strip():
            return mappings

        # Split by semicolon and process each mapping
        mapping_pairs = [pair.strip() for pair in mappings_env.split(";") if pair.strip()]

        for pair in mapping_pairs:
            if "," not in pair:
                raise PathMappingError(f"Invalid mapping format: '{pair}'. Expected 'source,destination'")

            # Split on comma
            parts = pair.split(",", 1)
            if len(parts) != pair_length:
                raise PathMappingError(f"Invalid mapping format: '{pair}'. Expected 'source,destination'")

            source, destination = parts[0].strip(), parts[1].strip()

            if not source or not destination:
                raise PathMappingError(f"Empty source or destination in mapping: '{pair}'")

            normalized_source = self._normalize_path(source)
            normalized_destination = self._normalize_path(destination)
            is_windows_source = self._is_path_windows(normalized_source)
            is_windows_destination = self._is_path_windows(normalized_destination)

            # Categorize the mapping
            if is_windows_source != is_windows_destination:
                category = "cross-platform"
            elif is_windows_source and is_windows_destination:
                category = "windows"
            else:
                category = "linux"

            # Normalize paths for consistent matching
            mappings[category][normalized_source] = normalized_destination
            mappings[category][normalized_destination] = normalized_source

        return mappings

    def _normalize_path(self, path_str: str) -> str:
        """Normalize a path string for consistent mapping lookup.

        Args:
            path_str (str): path string to normalize.

        Returns:
            str: normalized path string.
        """
        # Convert backslashes to forward slashes and remove trailing slashes
        return path_str.replace("\\", "/").rstrip("/")

    def _is_path_windows(self, path_str: str) -> bool:
        """Determine if path appears to be a Windows path.

        Args:
            path_str (str | Path): path string to analyze.

        Returns:
            bool: True if path appears to be Windows format.
        """
        drive_letter_min_length = 2

        # Check for Windows-specific patterns
        windows_indicators = (
            # Drive letter pattern (C:, D:, etc.)
            len(path_str) >= drive_letter_min_length and path_str[1] == ":" and path_str[0].isalpha(),
            # Backslash separators
            "\\" in path_str,
            # UNC path pattern (\\server\share)
            path_str.startswith("\\\\"),
        )

        return any(windows_indicators)

    def _find_mapping(self, path_str: str, category: str = "cross-platform") -> str | None:
        """Find a mapping for the given path string.

        Args:
            path_str (str): path string to find mapping for.
            category (str): category for mapping lookup. Defaults to cross-platform.

        Returns:
            str: mapped path if found, None otherwise.
        """
        normalized_path = self._normalize_path(path_str)
        mappings = self._mappings[category]

        # Direct match first
        if normalized_path in mappings:
            return mappings[normalized_path]

        # Check for prefix matches (longest match wins)
        matching_mappings = [(source, target) for source, target in mappings.items() if normalized_path.startswith(source + "/") or normalized_path == source]

        if not matching_mappings:
            return None

        # Sort by prefix length (descending) to get longest match
        matching_mappings.sort(key=lambda x: len(x[0]), reverse=True)
        best_source, best_target = matching_mappings[0]

        # Replace the prefix with the mapping
        relative_part = normalized_path[len(best_source) :].lstrip("/")
        return f"{best_target}/{relative_part}" if relative_part else best_target

    def to_path(self, path: str | Path, mapping: bool, target: str = "auto") -> str:
        """Translate path to appropriate Path object based on mapping rules, as well as native system or target.

        Args:
            path (str | Path): string or Path object to translate.
            mapping (bool): whether to apply mapping.
            target (str): target system to convert input path to. Defaults to auto.

        Returns:
            str: translated path as string.

        Raises:
            PathTranslationError: if required mapping is not found.
        """
        path_str = str(path) if isinstance(path, Path) else path
        if not path_str:
            raise PathTranslationError("Path must be a non-empty string")

        if target not in self._valid_targets:
            raise PathTranslationError(f"Invalid target: '{target}'. Must be one of {self._valid_targets}")

        path_system = "windows" if self._is_path_windows(path_str) else "linux"
        target_system = self._system if target == "auto" else target

        # Case 1: Same system type (Linux->Linux or Windows->Windows)
        if path_system == target_system:
            if mapping:
                mapped_path = self._find_mapping(path_str, target)
                if mapped_path:
                    path_str = mapped_path

            return path_str

        # Case 2: Cross-platform conversion required (mapping is mandatory)
        mapped_path = self._find_mapping(path_str, "cross-platform")
        if not mapped_path:
            raise PathTranslationError(f"No {target_system.capitalize()} mapping found for {path_system.capitalize()} path: '{path_str}'")

        return mapped_path


# Global instance for easy access
_translator_instance = None


def translator() -> PathTranslator:
    """Get global instance.

    Returns:
        PathTranslator: path translator instance.
    """
    global _translator_instance
    if _translator_instance is None:
        _translator_instance = PathTranslator(environ.get("MAPPINGS_PATH", default="C:\\,/mnt/"))
    return _translator_instance


# ---------------------------------------------------------------------------- #
#               ------- System ------
# ---------------------------------------------------------------------------- #
def to_path(path: str | Path, mapping: bool = False) -> Path:
    """Translate path to native system format with optional mapping.

    Args:
        path (str | Path): path to translate.
        mapping (bool, optional): whether to apply mapping. Defaults to False.

    Returns:
        Path: Native system translated path.
    """
    return Path(translator().to_path(path, mapping=mapping))


def to_pure_path(path: str | Path, mapping: bool = False) -> PurePosixPath | PureWindowsPath:
    """Translate path to native system pure format with optional mapping.

    Args:
        path (str | Path): path to translate.
        mapping (bool, optional): whether to apply mapping. Defaults to False.

    Returns:
        Path: Native system translated pure path.
    """
    target_system = "linux" if system() in ("Linux", "Darwin") else "windows"
    if target_system == "windows":
        return PureWindowsPath(translator().to_path(path, mapping=mapping))
    return PurePosixPath(translator().to_path(path, mapping=mapping))


# ---------------------------------------------------------------------------- #
#               ------- Linux ------
# ---------------------------------------------------------------------------- #
def to_posix(path: str | Path, mapping: bool = True) -> Path:
    """Translate a path to Posix format.

    Args:
        path (str | Path): path to translate.
        mapping (bool, optional): whether to apply mapping. Defaults to True.

    Returns:
        Path: Posix translated path.
    """
    return Path(translator().to_path(path, mapping=mapping, target="linux"))


def to_pure_posix(path: str | Path, mapping: bool = True) -> PurePosixPath:
    """Translate a path to Posix pure format.

    Args:
        path (str | Path): path to translate.
        mapping (bool, optional): whether to apply mapping. Defaults to True.

    Returns:
        PurePosixPath: Posix translated pure path.
    """
    return PurePosixPath(translator().to_path(path, mapping=mapping, target="linux"))


# ---------------------------------------------------------------------------- #
#               ------- Windows ------
# ---------------------------------------------------------------------------- #
def to_windows(path: str | Path, mapping: bool = True) -> Path:
    """Translate a path to Windows format.

    Args:
        path (str | Path): path to translate.
        mapping (bool, optional): whether to apply mapping. Defaults to True.

    Returns:
        Path: Windows translated path.
    """
    return Path(translator().to_path(path, mapping=mapping, target="windows"))


def to_pure_windows(path: str | Path, mapping: bool = True) -> PureWindowsPath:
    """Translate a path to Windows pure format.

    Args:
        path (str | Path): path to translate.
        mapping (bool, optional): whether to apply mapping. Defaults to True.

    Returns:
        PureWindowsPath: Windows translated pure path.
    """
    return PureWindowsPath(translator().to_path(path, mapping=mapping, target="windows"))
