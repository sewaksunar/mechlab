"""Core utilities: base classes, registries, and configuration.

This module provides the foundation for all MechLab components:
  - Base classes: EngineeringBase, PhysicsObject
  - Mixins: AnimatableMixin, ExportableMixin
  - Registry system for auto-discovery
  - Configuration management
  - Type definitions
"""

from .base import (
    # Types
    Number,
    Vector2D,
    Vector3D,
    TimeArray,
    StateArray,
    # Registry
    Registry,
    physics_registry,
    animation_registry,
    solver_registry,
    # Base classes
    EngineeringBase,
    PhysicsObject,
    PhysicsState,
    # Mixins
    Animatable,
    AnimatableMixin,
    ExportableMixin,
    # Config
    MechLabConfig,
    config,
    # Utilities
    ensure_vector3d,
    magnitude,
)

# Backward compatibility with old imports
from mechlab.units import STRESS_UNITS, to_base, from_base

__all__ = [
    # Types
    "Number",
    "Vector2D",
    "Vector3D",
    "TimeArray",
    "StateArray",
    # Registry
    "Registry",
    "physics_registry",
    "animation_registry",
    "solver_registry",
    # Base classes
    "EngineeringBase",
    "PhysicsObject",
    "PhysicsState",
    # Mixins
    "Animatable",
    "AnimatableMixin",
    "ExportableMixin",
    # Config
    "MechLabConfig",
    "config",
    # Utilities
    "ensure_vector3d",
    "magnitude",
    # Legacy
    "STRESS_UNITS",
    "to_base",
    "from_base",
]
