"""Shared CLI utilities for argument parsing and validation."""

from __future__ import annotations

from typing import Callable, TypeVar, overload

T = TypeVar("T")


def get_flag(
    args: list[str],
    name: str,
    default: T | None = None,
    cast: Callable[[str], T] | None = float,
) -> T | None:
    """
    Extract a flag value from command-line arguments.

    Args:
        args: List of command-line arguments
        name: Flag name to search for (e.g., '--sx')
        default: Default value if flag not found
        cast: Function to convert string value (default: float)

    Returns:
        Parsed value or default if not found

    Example:
        >>> get_flag(['--sx', '100', '--sy', '50'], '--sx')
        100.0
    """
    args_list = list(args)
    if name not in args_list:
        return default

    idx = args_list.index(name)
    if idx + 1 >= len(args_list):
        return default

    value = args_list[idx + 1]
    try:
        return cast(value) if cast else value  # type: ignore[return-value]
    except (ValueError, TypeError):
        return default


def get_str(args: list[str], name: str) -> str | None:
    """
    Extract a string flag value from command-line arguments.

    Args:
        args: List of command-line arguments
        name: Flag name to search for

    Returns:
        String value or None if not found
    """
    return get_flag(args, name, default=None, cast=str)


def has_flag(args: list[str], *names: str) -> bool:
    """
    Check if any of the given flags are present.

    Args:
        args: List of command-line arguments
        names: Flag names to check (e.g., '-h', '--help')

    Returns:
        True if any flag is present
    """
    return any(name in args for name in names)


def print_error(message: str) -> None:
    """Print an error message with formatting."""
    print(f"❌ Error: {message}")


def print_success(message: str) -> None:
    """Print a success message with formatting."""
    print(f"✔ {message}")
