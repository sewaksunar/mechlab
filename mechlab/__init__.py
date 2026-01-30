"""MechLab: A Modular Mechanical Engineering Laboratory for Python.

Provides unified interfaces for:
  - Mechanics (statics & dynamics)
  - Thermodynamics (properties & cycles)
  - Fluid Mechanics
  - Control Systems
  - Numerical & Symbolic Computation
"""

from . import mechanics
from . import thermodynamics
from . import units
from . import math
from . import core
from . import display
from . import export
from . import interactive
from . import visual

__version__ = "0.2.4"
__author__ = "Sewak Sunar"
__license__ = "MIT"

__all__ = [
    "mechanics",
    "thermodynamics",
    "units",
    "math",
    "core",
    "display",
    "export",
    "interactive",
    "visual",
]
