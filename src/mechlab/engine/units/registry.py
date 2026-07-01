"""
engine.units.registry — a minimal unit-conversion system.

Internally, mechlab always works in SI base units (meters, newtons,
pascals, kilograms, seconds). This module exists so *input/output*
can be given in other common engineering units without polluting the
domain layer with unit-awareness.

Example:
    >>> from mechlab.engine.units.registry import UnitRegistry
    >>> ur = UnitRegistry()
    >>> ur.to_si(50, "kN")
    50000.0
    >>> ur.from_si(50000, "kN")
    50.0
"""

from __future__ import annotations


class UnitRegistry:
    """
    Holds conversion factors to/from SI base units.

    Each entry maps a unit symbol -> multiplier such that:
        si_value = input_value * factor
        input_value = si_value / factor

    Attributes:
        _factors: internal mapping of unit symbol to SI multiplier.
    """

    def __init__(self) -> None:
        self._factors: dict[str, float] = {
            # length (-> meters)
            "m": 1.0,
            "mm": 1e-3,
            "cm": 1e-2,
            "in": 0.0254,
            "ft": 0.3048,
            # force (-> newtons)
            "N": 1.0,
            "kN": 1e3,
            "lbf": 4.4482216153,
            # pressure / stress (-> pascals)
            "Pa": 1.0,
            "kPa": 1e3,
            "MPa": 1e6,
            "GPa": 1e9,
            "psi": 6894.757293168,
        }

    def register(self, symbol: str, si_factor: float) -> None:
        """Add or override a unit's SI conversion factor.

        Args:
            symbol: unit symbol, e.g. "kip".
            si_factor: multiplier such that value_in_symbol * si_factor = value_in_SI.
        """
        self._factors[symbol] = si_factor

    def to_si(self, value: float, unit: str) -> float:
        """Convert a value FROM the given unit TO SI base units."""
        self._assert_known(unit)
        return value * self._factors[unit]

    def from_si(self, si_value: float, unit: str) -> float:
        """Convert a value FROM SI base units TO the given unit."""
        self._assert_known(unit)
        return si_value / self._factors[unit]

    def _assert_known(self, unit: str) -> None:
        if unit not in self._factors:
            known = ", ".join(sorted(self._factors))
            raise ValueError(f"Unknown unit '{unit}'. Known units: {known}")
