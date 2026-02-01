"""Unit registry for engineering calculations.

Defines conversion factors to SI base units:
  - Length: meter (m)
  - Force: newton (N)
  - Pressure: pascal (Pa)
  - Mass: kilogram (kg)
"""

from __future__ import annotations

UNITS: dict[str, dict[str, float]] = {
    "length": {
        "m": 1.0,
        "mm": 1e-3,
        "cm": 1e-2,
        "km": 1e3,
        "inch": 0.0254,
        "ft": 0.3048,
        "yd": 0.9144,
    },
    "force": {
        "N": 1.0,
        "kN": 1e3,
        "MN": 1e6,
        "lbf": 4.44822,
        "kgf": 9.80665,
    },
    "pressure": {
        "Pa": 1.0,
        "kPa": 1e3,
        "MPa": 1e6,
        "GPa": 1e9,
        "bar": 1e5,
        "psi": 6894.76,
        "ksi": 6894760.0,
    },
    "mass": {
        "kg": 1.0,
        "g": 1e-3,
        "mg": 1e-6,
        "ton": 1e3,
        "lb": 0.453592,
        "oz": 0.0283495,
    },
    "area": {
        "m2": 1.0,
        "mm2": 1e-6,
        "cm2": 1e-4,
        "in2": 6.4516e-4,
        "ft2": 0.092903,
    },
    "moment": {
        "Nm": 1.0,
        "kNm": 1e3,
        "lbf_ft": 1.35582,
        "lbf_in": 0.112985,
    },
}

# Alias for stress units (flat dict for backward compatibility)
STRESS_UNITS: dict[str, float] = UNITS["pressure"]


def to_base(value: float, unit: str) -> float:
    """Convert stress value to base unit (Pascal)."""
    return value * STRESS_UNITS[unit]


def from_base(value: float, unit: str) -> float:
    """Convert stress value from base unit (Pascal) to specified unit."""
    return value / STRESS_UNITS[unit]
