"""Base classes for engineering calculations.

This module provides the foundation for all MechLab objects:
  - EngineeringBase: Core base class with symbolic support
  - PhysicsObject: Base for all physical entities (particles, bodies, etc.)
  - AnimatableMixin: Mixin for objects that can be animated
  - ExportableMixin: Mixin for objects with data export capabilities
  - Registry: Auto-discovery and factory pattern implementation

Design Principles:
  - DRY: Common functionality in base classes/mixins
  - Composition over inheritance where appropriate
  - Consistent naming via __registry_name__
  - Automatic feature discovery
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import (
    Any,
    Callable,
    ClassVar,
    Dict,
    Generic,
    Iterator,
    List,
    Optional,
    Protocol,
    Tuple,
    Type,
    TypeVar,
    Union,
    runtime_checkable,
)
import json
from pathlib import Path

import numpy as np
import sympy as sp

# Type aliases
Number = Union[int, float, sp.Expr]
Vector2D = Tuple[float, float]
Vector3D = Tuple[float, float, float]
TimeArray = np.ndarray
StateArray = np.ndarray

T = TypeVar("T")


# =============================================================================
# REGISTRY SYSTEM - Auto-discovery and factory pattern
# =============================================================================

class Registry(Generic[T]):
    """Generic registry for auto-discovery of classes.

    Provides factory pattern with automatic registration via decorators
    or metaclass. Eliminates need for manual imports and reduces coupling.

    Example:
        >>> physics_registry = Registry[PhysicsObject]("physics")
        >>> @physics_registry.register("projectile")
        ... class Projectile(PhysicsObject):
        ...     pass
        >>> proj = physics_registry.create("projectile", velocity=(10, 10, 0))
    """

    _instances: ClassVar[Dict[str, "Registry"]] = {}

    def __init__(self, name: str) -> None:
        self.name = name
        self._registry: Dict[str, Type[T]] = {}
        self._metadata: Dict[str, Dict[str, Any]] = {}
        Registry._instances[name] = self

    def register(
        self,
        name: Optional[str] = None,
        **metadata: Any,
    ) -> Callable[[Type[T]], Type[T]]:
        """Decorator to register a class.

        Args:
            name: Registry name (defaults to class.__name__)
            **metadata: Additional metadata (description, category, etc.)
        """
        def decorator(cls: Type[T]) -> Type[T]:
            key = name or cls.__name__
            self._registry[key] = cls
            self._metadata[key] = {
                "class": cls,
                "module": cls.__module__,
                **metadata,
            }
            # Store registry reference on class
            cls.__registry_name__ = key  # type: ignore
            cls.__registry__ = self  # type: ignore
            return cls
        return decorator

    def create(self, name: str, *args: Any, **kwargs: Any) -> T:
        """Factory method to create registered objects.

        Args:
            name: Registered name
            *args, **kwargs: Constructor arguments

        Returns:
            New instance of registered class
        """
        if name not in self._registry:
            available = ", ".join(self._registry.keys())
            raise KeyError(f"Unknown '{name}'. Available: {available}")
        return self._registry[name](*args, **kwargs)

    def get(self, name: str) -> Type[T]:
        """Get class by name without instantiating."""
        return self._registry[name]

    def list(self) -> List[str]:
        """List all registered names."""
        return list(self._registry.keys())

    def metadata(self, name: str) -> Dict[str, Any]:
        """Get metadata for registered class."""
        return self._metadata.get(name, {})

    def __contains__(self, name: str) -> bool:
        return name in self._registry

    def __iter__(self) -> Iterator[str]:
        return iter(self._registry)

    def __len__(self) -> int:
        return len(self._registry)

    @classmethod
    def get_registry(cls, name: str) -> "Registry":
        """Get registry by name."""
        return cls._instances[name]


# Global registries
physics_registry = Registry[Any]("physics")
animation_registry = Registry[Any]("animation")
solver_registry = Registry[Any]("solver")


# =============================================================================
# BASE CLASSES
# =============================================================================

class EngineeringBase(ABC):
    """Base class for all engineering objects with symbolic support.

    Provides:
      - Symbolic expression detection
      - Consistent string representation
      - Serialization support
      - Validation hooks
    """

    def is_symbolic(self) -> bool:
        """Check if any attributes contain symbolic expressions."""
        for v in self.__dict__.values():
            if isinstance(v, sp.Expr):
                return True
            if isinstance(v, (list, tuple)):
                if any(isinstance(x, sp.Expr) for x in v):
                    return True
        return False

    def to_symbolic(self) -> "EngineeringBase":
        """Convert object to symbolic representation."""
        raise NotImplementedError("Subclasses must implement to_symbolic()")

    def to_numeric(self, subs: Optional[Dict[sp.Symbol, float]] = None) -> "EngineeringBase":
        """Convert symbolic expressions to numeric values."""
        raise NotImplementedError("Subclasses must implement to_numeric()")

    def validate(self) -> bool:
        """Validate object state. Override in subclasses."""
        return True

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "__class__": self.__class__.__name__,
            "__module__": self.__class__.__module__,
            **{k: self._serialize_value(v) for k, v in self.__dict__.items()},
        }

    @staticmethod
    def _serialize_value(value: Any) -> Any:
        """Serialize a single value."""
        if isinstance(value, np.ndarray):
            return {"__ndarray__": value.tolist()}
        if isinstance(value, sp.Expr):
            return {"__sympy__": str(value)}
        if isinstance(value, (tuple, list)):
            return [EngineeringBase._serialize_value(v) for v in value]
        return value

    def __repr__(self) -> str:
        attrs = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items()
                         if not k.startswith("_"))
        return f"{self.__class__.__name__}({attrs})"


# =============================================================================
# PHYSICS OBJECT BASE
# =============================================================================

@dataclass
class PhysicsState:
    """Represents the state of a physics object at a point in time.

    Immutable snapshot of position, velocity, and derived quantities.
    """
    time: float
    position: Vector3D
    velocity: Vector3D
    acceleration: Vector3D = (0.0, 0.0, 0.0)
    energy: Optional[Dict[str, float]] = None

    def to_array(self) -> np.ndarray:
        """Convert to numpy array [t, x, y, z, vx, vy, vz, ax, ay, az]."""
        return np.array([
            self.time,
            *self.position,
            *self.velocity,
            *self.acceleration,
        ])


class PhysicsObject(EngineeringBase):
    """Base class for all physical entities in dynamics/kinematics.

    Provides unified interface for:
      - State management (position, velocity, acceleration)
      - Time evolution (trajectory calculation)
      - Energy computation
      - State queries at arbitrary times

    Subclasses must implement:
      - state_at_time(t): Return PhysicsState at time t
      - time_span(): Return valid time range
    """

    # Class-level defaults
    DEFAULT_G: ClassVar[float] = 9.81
    DEFAULT_NUM_POINTS: ClassVar[int] = 200

    def __init__(
        self,
        position: Vector3D = (0.0, 0.0, 0.0),
        velocity: Vector3D = (0.0, 0.0, 0.0),
        mass: float = 1.0,
        **kwargs: Any,
    ) -> None:
        self.position = tuple(float(x) for x in position)
        self.velocity = tuple(float(x) for x in velocity)
        self.mass = float(mass)
        self._trajectory_cache: Optional[Tuple[TimeArray, StateArray, StateArray]] = None

    @property
    def speed(self) -> float:
        """Magnitude of velocity vector."""
        return float(np.linalg.norm(self.velocity))

    def kinetic_energy(self) -> float:
        """Calculate kinetic energy: KE = ½mv²."""
        return 0.5 * self.mass * self.speed ** 2

    @abstractmethod
    def state_at_time(self, t: float) -> PhysicsState:
        """Get complete state at time t."""
        pass

    @abstractmethod
    def time_span(self) -> Tuple[float, float]:
        """Return (t_start, t_end) for valid time range."""
        pass

    def trajectory(
        self,
        num_points: Optional[int] = None,
    ) -> Tuple[TimeArray, StateArray, StateArray]:
        """Generate trajectory arrays.

        Returns:
            (t_array, positions[N,3], velocities[N,3])
        """
        if self._trajectory_cache is not None:
            return self._trajectory_cache

        n = num_points or self.DEFAULT_NUM_POINTS
        t_start, t_end = self.time_span()

        if t_end <= t_start:
            return (
                np.array([t_start]),
                np.array([self.position]),
                np.array([self.velocity]),
            )

        t_array = np.linspace(t_start, t_end, n)
        positions = np.array([self.state_at_time(t).position for t in t_array])
        velocities = np.array([self.state_at_time(t).velocity for t in t_array])

        self._trajectory_cache = (t_array, positions, velocities)
        return self._trajectory_cache

    def invalidate_cache(self) -> None:
        """Clear cached trajectory (call after modifying state)."""
        self._trajectory_cache = None


# =============================================================================
# MIXINS - Composable functionality
# =============================================================================

@runtime_checkable
class Animatable(Protocol):
    """Protocol for objects that can be animated."""

    def trajectory(
        self, num_points: Optional[int] = None
    ) -> Tuple[TimeArray, StateArray, StateArray]:
        """Return (t_array, positions, velocities)."""
        ...

    def time_span(self) -> Tuple[float, float]:
        """Return valid time range."""
        ...


class AnimatableMixin:
    """Mixin providing animation data generation.

    Requires the class to have trajectory() and time_span() methods.
    Provides standardized animation frame generation.
    """

    def animation_frames(
        self: Animatable,
        fps: int = 30,
        duration: Optional[float] = None,
    ) -> Iterator[PhysicsState]:
        """Generate animation frames at specified FPS.

        Args:
            fps: Frames per second
            duration: Override duration (defaults to time_span)

        Yields:
            PhysicsState for each frame
        """
        t_start, t_end = self.time_span()
        dur = duration or (t_end - t_start)

        if dur <= 0:
            return

        num_frames = int(dur * fps)
        for i in range(num_frames + 1):
            t = t_start + (i / fps)
            if hasattr(self, "state_at_time"):
                yield self.state_at_time(t)  # type: ignore

    def animation_data(
        self: Animatable,
        num_points: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get all data needed for animation.

        Returns:
            Dict with t_array, positions, velocities, and metadata
        """
        t_array, positions, velocities = self.trajectory(num_points)
        t_start, t_end = self.time_span()

        return {
            "t_array": t_array,
            "positions": positions,
            "velocities": velocities,
            "t_start": t_start,
            "t_end": t_end,
            "duration": t_end - t_start,
            "num_frames": len(t_array),
        }


class ExportableMixin:
    """Mixin providing data export capabilities."""

    def to_csv(self, filename: str, **kwargs: Any) -> None:
        """Export trajectory to CSV file."""
        if not hasattr(self, "trajectory"):
            raise NotImplementedError("Object must have trajectory() method")

        t_array, positions, velocities = self.trajectory()  # type: ignore

        data = np.column_stack([t_array, positions, velocities])
        header = "time,x,y,z,vx,vy,vz"

        np.savetxt(filename, data, delimiter=",", header=header, comments="", **kwargs)
        print(f"✔ Exported to {filename}")

    def to_json(self, filename: str) -> None:
        """Export object state to JSON."""
        data = self.to_dict() if hasattr(self, "to_dict") else self.__dict__

        # Convert numpy arrays
        def convert(obj: Any) -> Any:
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            if isinstance(obj, dict):
                return {k: convert(v) for k, v in obj.items()}
            if isinstance(obj, (list, tuple)):
                return [convert(v) for v in obj]
            return obj

        with open(filename, "w") as f:
            json.dump(convert(data), f, indent=2)
        print(f"✔ Exported to {filename}")


# =============================================================================
# CONFIGURATION SYSTEM
# =============================================================================

@dataclass
class MechLabConfig:
    """Global configuration for MechLab.

    Centralized settings for defaults, units, and behavior.
    """
    # Physics defaults
    gravity: float = 9.81
    default_mass: float = 1.0

    # Animation defaults
    animation_fps: int = 30
    animation_dpi: int = 100
    default_figsize: Tuple[float, float] = (12, 8)

    # Export settings
    mp4_writer: str = "ffmpeg"
    gif_writer: str = "pillow"

    # Numerical settings
    trajectory_points: int = 200
    tolerance: float = 1e-9

    # Display settings
    unit_system: str = "SI"  # SI, Imperial, CGS

    @classmethod
    def load(cls, path: Union[str, Path]) -> "MechLabConfig":
        """Load config from JSON file."""
        with open(path) as f:
            data = json.load(f)
        return cls(**data)

    def save(self, path: Union[str, Path]) -> None:
        """Save config to JSON file."""
        with open(path, "w") as f:
            json.dump(self.__dict__, f, indent=2)


# Global config instance
config = MechLabConfig()


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def ensure_vector3d(v: Any) -> Vector3D:
    """Convert input to 3D vector tuple."""
    if isinstance(v, (list, tuple, np.ndarray)):
        if len(v) == 2:
            return (float(v[0]), float(v[1]), 0.0)
        if len(v) == 3:
            return (float(v[0]), float(v[1]), float(v[2]))
    raise ValueError(f"Cannot convert {v} to Vector3D")


def magnitude(v: Union[Vector2D, Vector3D, np.ndarray]) -> float:
    """Calculate magnitude of vector."""
    return float(np.linalg.norm(v))


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
]
