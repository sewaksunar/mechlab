"""Core utilities: base classes and unit helpers.

Re-exports unit functions from mechlab.units for backward compatibility.
"""

from mechlab.units import STRESS_UNITS, to_base, from_base
from .base import EngineeringBase, Number

__all__ = [
    "STRESS_UNITS",
    "to_base",
    "from_base",
    "EngineeringBase",
    "Number",
]
