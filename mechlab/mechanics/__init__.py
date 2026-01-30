"""Mechanics: statics, dynamics, and stress analysis.

Core models for:
  - Static structural analysis (beams, plates, particles)
  - Rigid body dynamics
  - Stress state and tensor analysis
"""

from .dynamics import RigidBody
from .statics import Beam, StaticsParticle
from .statics.stress import StressTensor3D, StressTransform, PrincipalStresses
from .stress import StressState

__all__ = [
    "RigidBody",
    "Beam",
    "StressTensor3D",
    "StressTransform",
    "PrincipalStresses",
    "StaticsParticle",
    "StressState",
]