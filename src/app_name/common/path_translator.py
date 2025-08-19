#!/usr/bin/env python3
"""Module used to interact with Linux and Windows paths.

This module provides utilities for translating paths between Linux and Windows
formats using configurable path mappings. It handles cross-platform path
conversion while maintaining proper path semantics.
"""

# Standard Library
from pathlib import Path, PurePath, PurePosixPath, PureWindowsPath


class PathTranslationError(Exception):
    """Custom exception for path translation errors."""

    pass


class PathTranslator:
    """Handle path translation between Windows and Linux formats.

    This class encapsulates path mapping logic and provides methods for
    bidirectional path translation with proper validation and error handling.

    Attributes:
        mappings (dict[Path, Path]): Dictionary mapping Windows paths to Linux paths.
    """

    def __init__(self, mappings: str = "") -> None:
        """Initialize class."""
        self.mappings = self._normalize_mappings(mappings)

    def _normalize_mappings(self, mappings_str: str) -> dict[PureWindowsPath, PurePosixPath]:
        r"""Normalize and validate path mappings.

        Each mapping is separated by a semicolon, e.g., "C:\\path:/mnt/c/path;D:\\path:/mnt/d/path"

        Args:
            mappings_str (str): Raw mappings to normalize.

        Returns:
            dict[Path, Path]: Normalized mappings with Path objects.

        Raises:
            PathTranslationError: If mappings are invalid.
        """
        colon_count = 2
        normalized = {}

        for mapping in mappings_str.split(";"):
            if mapping.count(":") != colon_count:
                raise ValueError(f"MAPPINGS_PATH element is not formatted correctly ({mapping})")
            parts = mapping.rsplit(":", 1)
            win_path = parts[0]
            linux_path = parts[1]

            try:
                win_key = PureWindowsPath(win_path)
                linux_value = PurePosixPath(linux_path)
                normalized[win_key] = linux_value
            except (TypeError, ValueError) as err:
                raise PathTranslationError(f"Invalid mapping '{win_path}' -> '{linux_path}': {err}") from err

        return normalized

    @staticmethod
    def _is_windows(path: str | Path) -> bool:
        """Check if a path follows Windows conventions.

        Args:
            path (str | Path): Path to check.

        Returns:
            bool: True if path has Windows format (drive letter), False otherwise.
        """
        try:
            return bool(PureWindowsPath(path).drive)
        except (TypeError, ValueError):
            return False

    def _find_best_mapping(self, path: Path, reverse: bool = False) -> tuple[PurePath, PurePath, int] | None:
        """Find the best matching mapping for a given path.

        Args:
            path (Path): Path to find mapping for.
            reverse (bool): If True, map from Linux to Windows; otherwise Windows to Linux.

        Returns:
            tuple[Path, Path, int] | None: Tuple of (source, target, prefix_length) if found,
                None otherwise.
        """
        path_parts = [part.lower() for part in path.parts]
        best_match = None
        max_length = 0

        for win_path, linux_path in self.mappings.items():
            source, target = (linux_path, win_path) if reverse else (win_path, linux_path)

            try:
                source_parts = [part.lower() for part in Path(source).parts]
            except (TypeError, ValueError):
                continue

            # Check if source is a prefix and find longest match
            if len(source_parts) <= len(path_parts) and len(source_parts) > max_length and source_parts == path_parts[: len(source_parts)]:
                best_match = (source, target, len(source_parts))
                max_length = len(source_parts)

        return best_match

    def _translate(self, path_str: str, to_windows: bool = False) -> Path:
        """Core path translation logic.

        Args:
            path_str (str): Path string to translate.
            to_windows (bool): If True, translate to Windows format; otherwise to Linux.

        Returns:
            Path: Translated path.

        Raises:
            PathTranslationError: If translation fails.
        """
        if not isinstance(path_str, str) or not path_str.strip():
            raise PathTranslationError("Path must be a non-empty string")

        try:
            # Try to resolve path, but don't fail if it doesn't exist
            try:
                path = Path(path_str).resolve()
            except OSError:
                path = Path(path_str)

        except (TypeError, ValueError) as err:
            raise PathTranslationError(f"Invalid path '{path_str}': {err}") from err

        # Determine if translation is needed
        is_win_path = self._is_windows(path)
        needs_translation = (to_windows and not is_win_path) or (not to_windows and is_win_path)

        if not needs_translation:
            return path

        # Find matching mapping
        match = self._find_best_mapping(path, reverse=to_windows)
        if not match:
            return path

        source, target, prefix_length = match
        remaining_parts = path.parts[prefix_length:]

        # Construct translated path
        return Path(target) / Path(*remaining_parts) if remaining_parts else Path(target)

    def to_linux(self, path: str | Path) -> Path:
        """Translate a path to Linux format.

        Args:
            path (str | Path): Path to translate.

        Returns:
            Path: Path in Linux format.
        """
        if isinstance(path, Path):
            path = str(path)
        return self._translate(path, to_windows=False)

    def to_windows(self, path: str | Path) -> PureWindowsPath:
        """Translate a path to Windows format.

        Args:
            path (str | Path): Path to translate.

        Returns:
            PureWindowsPath: Path in Windows format.
        """
        if isinstance(path, Path):
            path = str(path)
        return PureWindowsPath(self._translate(path, to_windows=True))
