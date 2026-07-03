"""
Core domain entities — pure data + behavior, no I/O, no external deps.
This is the OOP backbone: everything downstream (statics, dynamics,
strength) builds on these classes.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum

# --------------------------------------------------------------------------
# Material & Section — reusable value objects
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class Material:
    """Immutable material properties."""
    name: str
    young_modulus: float      # E, in Pa
    yield_strength: float     # in Pa

    def __post_init__(self) -> None:
        if self.young_modulus <= 0:
            raise ValueError("young_modulus must be positive")


@dataclass(frozen=True)
class Section:
    """Cross-sectional geometric properties."""
    name: str
    moment_of_inertia: float   # I, in m^4
    area: float                 # in m^2
    extreme_fiber_distance: float  # c, distance to outer fiber, in m

    def section_modulus(self) -> float:
        """Z = I / c — used for bending stress calcs."""
        return self.moment_of_inertia / self.extreme_fiber_distance


# --------------------------------------------------------------------------
# Load hierarchy — abstract base + concrete types (OOP polymorphism)
# --------------------------------------------------------------------------

class Load(ABC):
    """Abstract base for any load acting on a Body."""

    def __init__(self, position: float):
        self.position = position  # location along the body, in m

    @abstractmethod
    def total_force(self) -> float:
        """Resultant force magnitude (N), downward positive."""
        raise NotImplementedError

    @abstractmethod
    def moment_about(self, ref_position: float) -> float:
        """Moment this load creates about a reference point (N·m)."""
        raise NotImplementedError


class PointLoad(Load):
    def __init__(self, position: float, magnitude: float):
        super().__init__(position)
        self.magnitude = magnitude  # N, downward positive

    def total_force(self) -> float:
        return self.magnitude

    def moment_about(self, ref_position: float) -> float:
        return self.magnitude * (self.position - ref_position)

    def __repr__(self) -> str:
        return f"PointLoad({self.magnitude} N @ {self.position} m)"


class DistributedLoad(Load):
    """Uniformly distributed load over [start, end]."""

    def __init__(self, start: float, end: float, intensity: float):
        if end <= start:
            raise ValueError("end must be greater than start")
        super().__init__(position=(start + end) / 2)  # centroid
        self.start = start
        self.end = end
        self.intensity = intensity  # N/m

    def total_force(self) -> float:
        return self.intensity * (self.end - self.start)

    def moment_about(self, ref_position: float) -> float:
        return self.total_force() * (self.position - ref_position)

    def __repr__(self) -> str:
        return f"DistributedLoad({self.intensity} N/m, {self.start}-{self.end} m)"


# --------------------------------------------------------------------------
# Support — boundary conditions
# --------------------------------------------------------------------------

class SupportType(str, Enum):
    PIN = "pin"
    ROLLER = "roller"
    FIXED = "fixed"


@dataclass
class Support:
    position: float
    kind: str  # SupportType.PIN / ROLLER / FIXED
    reaction_force: float = 0.0
    reaction_moment: float = 0.0


# --------------------------------------------------------------------------
# Body — abstract base class for every physical object in the domain
# --------------------------------------------------------------------------

class Body(ABC):
    """
    Abstract base for anything analyzable: Beam, Truss, Shaft, etc.
    Subclasses must implement equilibrium-solving behavior.
    """

    def __init__(self, length: float, material: Material, section: Section):
        self.length = length
        self.material = material
        self.section = section
        self.loads: list[Load] = []
        self.supports: list[Support] = []

    def add_load(self, load: Load) -> Body:
        self.loads.append(load)
        return self  # enables method chaining

    def add_support(self, support: Support) -> Body:
        self.supports.append(support)
        return self

    @abstractmethod
    def solve(self) -> None:
        """Solve equilibrium / internal reactions. Implemented by subclass."""
        raise NotImplementedError
