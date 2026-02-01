"""Unit management: registry and conversions.

Provides:
  - UNITS: Full unit registry by category
  - STRESS_UNITS: Flat dict for stress units (backward compatible)
  - convert(): Convert between compatible units
  - to_base(), from_base(): Stress unit conversion helpers
"""

from .registry import UNITS, STRESS_UNITS, to_base, from_base
from .convert import convert, UnitError

__all__ = [
    "UNITS",
    "STRESS_UNITS",
    "convert",
    "UnitError",
    "to_base",
    "from_base",
]
