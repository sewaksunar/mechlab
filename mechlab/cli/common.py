"""Shared CLI utilities."""

from __future__ import annotations

from typing import Iterable, Callable, TypeVar

T = TypeVar("T")


def get_flag(args: Iterable[str], name: str, default: T | None = None, cast: Callable[[str], T] | None = float) -> T | None:
    """Return the value that follows a flag, or default if not present."""
    args_list = list(args)
    if name in args_list:
        idx = args_list.index(name)
        value = args_list[idx + 1]
        return cast(value) if cast else value  # type: ignore[arg-type]
    return default


def get_str(args: Iterable[str], name: str) -> str | None:
    """Return the string value that follows a flag, or None."""
    return get_flag(args, name, default=None, cast=str)
