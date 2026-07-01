"""
shared.utils — small, generic helpers with zero dependencies on the
rest of mechlab. Safe to import from any layer.
"""

from __future__ import annotations


def clamp(value: float, low: float, high: float) -> float:
    """Restrict `value` to the inclusive range [low, high].

    Args:
        value: input number.
        low: minimum allowed value.
        high: maximum allowed value.

    Returns:
        value, clamped into [low, high].

    Raises:
        ValueError: if low > high.
    """
    if low > high:
        raise ValueError("low must be <= high")
    return max(low, min(value, high))


def is_close(a: float, b: float, tol: float = 1e-9) -> bool:
    """Simple absolute-tolerance float comparison used across the codebase."""
    return abs(a - b) <= tol
