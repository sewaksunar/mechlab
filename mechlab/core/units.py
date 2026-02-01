"""Unit conversion utilities for stress and engineering quantities.

This module provides conversion functions between common stress units
and the SI base unit (Pascal).
"""

from __future__ import annotations

# Stress unit conversion factors to Pascal (Pa)
STRESS_UNITS: dict[str, float] = {
    "Pa": 1.0,
    "kPa": 1e3,
    "MPa": 1e6,
    "GPa": 1e9,
    "psi": 6894.76,
    "ksi": 6894760.0,
}


def to_base(value: float, unit: str) -> float:
    """
    Convert stress value to base unit (Pascal).

    Args:
        value: Stress value in specified unit
        unit: Unit name (Pa, kPa, MPa, GPa, psi, ksi)

    Returns:
        Stress value in Pascals

    Raises:
        KeyError: If unit is not recognized

    Example:
        >>> to_base(100, 'MPa')
        100000000.0
    """
    return value * STRESS_UNITS[unit]


def from_base(value: float, unit: str) -> float:
    """
    Convert stress value from base unit (Pascal) to specified unit.

    Args:
        value: Stress value in Pascals
        unit: Target unit name (Pa, kPa, MPa, GPa, psi, ksi)

    Returns:
        Stress value in target unit

    Raises:
        KeyError: If unit is not recognized

    Example:
        >>> from_base(100000000.0, 'MPa')
        100.0
    """
    return value / STRESS_UNITS[unit]
