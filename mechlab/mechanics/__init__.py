"""Mechanics: statics, dynamics, and stress analysis.

Core models for:
  - Plane stress analysis (StressState)
  - 3D stress tensors (StressTensor3D, StressTransform, PrincipalStresses)
  - Beam analysis (SimplySupportedBeam, Beam)
  - Particle statics (StaticsParticle)
  - Rigid body dynamics (RigidBody)

Example:
    >>> from mechlab.mechanics import StressState
    >>> state = StressState(100, 50, 25)
    >>> state.principal()
    (110.355..., 39.644...)
"""

from .stress import StressState
from .beam import SimplySupportedBeam
from .statics import Beam, StaticsParticle, StressTensor3D, StressTransform, PrincipalStresses
from .dynamics import RigidBody

__all__ = [
    # Stress analysis
    "StressState",
    "StressTensor3D",
    "StressTransform",
    "PrincipalStresses",
    # Beam analysis
    "SimplySupportedBeam",
    "Beam",
    # Statics
    "StaticsParticle",
    # Dynamics
    "RigidBody",
]