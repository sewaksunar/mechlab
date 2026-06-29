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

# Core submodules
from . import mechanics
from . import thermodynamics
from . import units
from . import math
from . import core
from . import design
from . import visual
from . import output

# Package metadata
__version__ = "0.2.4"
__author__ = "Sewak Sunar"
__license__ = "MIT"

__all__ = [
    # Core modules
    "mechanics",
    "thermodynamics",
    "units",
    "math",
    "core",
    "design",
    "visual",
    "output",
    # Metadata
    "__version__",
    "__author__",
    "__license__",
]


# Legacy aliases (deprecated - for backward compatibility)
def __getattr__(name: str):
    """Provide backward compatibility for removed modules."""
    if name == "display":
        import warnings
        warnings.warn(
            "mechlab.display is deprecated, use mechlab.output instead",
            DeprecationWarning,
            stacklevel=2,
        )
        from . import output
        return output
    if name == "interactive":
        import warnings
        warnings.warn(
            "mechlab.interactive is deprecated, use mechlab.visual.stress_widget instead",
            DeprecationWarning,
            stacklevel=2,
        )
        from . import visual
        return visual
    if name == "export":
        import warnings
        warnings.warn(
            "mechlab.export is deprecated, use mechlab.output instead",
            DeprecationWarning,
            stacklevel=2,
        )
        from . import output
        return output
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
