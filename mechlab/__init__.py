"""MechLab: A Modular Mechanical Engineering Laboratory for Python.

Provides unified interfaces for:
  - Mechanics (statics & dynamics)
  - Thermodynamics (properties & cycles)
  - Unit conversions
  - Mathematical calculations
  - Interactive visualizations

Quick Start:
    >>> import mechlab as ml
    >>> from mechlab.mechanics.stress import StressState
    >>> state = StressState(100, 50, 25)  # σx=100, σy=50, τxy=25 MPa
    >>> state.principal()  # Principal stresses
    (112.5, 37.5)

CLI Usage:
    $ mechlab --help
    $ mechlab stress compute --sx 100 --sy 50 --txy 25
    $ mechlab units convert 100 MPa psi
"""

from __future__ import annotations

# Submodules (lazy loading for faster startup)
from . import mechanics
from . import thermodynamics
from . import units
from . import math
from . import core
from . import display
from . import export
from . import interactive
from . import visual

# Package metadata
__version__ = "0.2.4"
__author__ = "Sewak Sunar"
__license__ = "MIT"
__email__ = ""

__all__ = [
    # Submodules
    "mechanics",
    "thermodynamics",
    "units",
    "math",
    "core",
    "display",
    "export",
    "interactive",
    "visual",
    # Metadata
    "__version__",
    "__author__",
    "__license__",
]
