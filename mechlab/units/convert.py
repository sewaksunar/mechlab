"""Unit conversion utilities.

Provides functions for converting between units of the same category.
"""

from __future__ import annotations

from mechlab.units.registry import UNITS


class UnitError(Exception):
    """Exception raised for unit conversion errors."""

    pass


def find_category(unit: str) -> str:
    """
    Find the category of a unit.

    Args:
        unit: Unit name to look up

    Returns:
        Category name (e.g., 'length', 'pressure')

    Raises:
        UnitError: If unit is not found in any category
    """
    for category, units in UNITS.items():
        if unit in units:
            return category
    raise UnitError(f"Unknown unit: {unit}")


def convert(value: float, from_unit: str, to_unit: str) -> float:
    """
    Convert a value from one unit to another.

    Args:
        value: Numeric value to convert
        from_unit: Source unit name
        to_unit: Target unit name

    Returns:
        Converted value

    Raises:
        UnitError: If units are unknown or incompatible

    Example:
        >>> convert(100, 'MPa', 'psi')
        14503.773773...
        >>> convert(1, 'm', 'ft')
        3.28084...
    """
    from_category = find_category(from_unit)
    to_category = find_category(to_unit)

    if from_category != to_category:
        raise UnitError(
            f"Incompatible units: {from_unit} ({from_category}) "
            f"cannot convert to {to_unit} ({to_category})"
        )

    # Convert: value -> SI base -> target
    base_value = value * UNITS[from_category][from_unit]
    return base_value / UNITS[to_category][to_unit]
