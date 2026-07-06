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

class PointMoment(Load):
    """
    A concentrated applied moment (couple) acting at a point.

    A pure couple has zero net force — it doesn't move the beam,
    only twists it — so total_force() is always 0. Its moment about
    *any* reference point is the couple's own magnitude, since a
    couple's moment is independent of the point you take it about.

    Sign convention: positive = counter-clockwise, in N·m.
    """

    def __init__(self, position: float, magnitude: float):
        super().__init__(position)
        self.magnitude = magnitude  # N·m, CCW positive

    def total_force(self) -> float:
        return 0.0

    def moment_about(self, ref_position: float) -> float:
        return self.magnitude

    def __repr__(self) -> str:
        return f"PointMoment({self.magnitude} N·m @ {self.position} m)"
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

# src/mechlab/domain/entities.py

@dataclass(frozen=True)
class DeflectionResult:
    positions: np.ndarray      # x-coordinates along the beam
    deflection: np.ndarray     # v(x), same units as length
    slope: np.ndarray          # v'(x), radians
    max_deflection: float
    max_deflection_location: float

"""
General geometric section-property calculator.

Works for ANY closed polygon (rectangle, circle approximation, triangle,
I-beam, L-angle, or a fully custom outline) using polygon integration
(shoelace-formula-based Green's theorem), plus composite shapes built
from multiple polygons (e.g. a solid outline minus one or more holes).

No shape-specific formulas are hardcoded here — a rectangle and a
hand-drawn arbitrary outline go through the exact same math.
"""


from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class SectionProperties:
    """All standard geometric properties of a 2D cross-section."""

    area: float
    centroid: tuple[float, float]

    # Centroidal (about the shape's own centroid) second moments of area
    Ixx: float          # about centroidal horizontal axis
    Iyy: float          # about centroidal vertical axis
    Ixy: float          # product of inertia
    J: float            # polar moment, J = Ixx + Iyy

    # Principal moments (Mohr's circle) — useful for unsymmetric shapes
    I_max: float
    I_min: float
    principal_angle_deg: float

    # Radii of gyration
    rx: float
    ry: float

    # Extreme fiber distances from centroid (for bending stress / section modulus)
    c_top: float
    c_bottom: float
    c_left: float
    c_right: float

    # Section moduli S = I / c
    Sx_top: float
    Sx_bottom: float
    Sy_left: float
    Sy_right: float

    perimeter: float
    vertices: np.ndarray  # the polygon(s) that were used, for plotting


def _raw_moments(vertices: np.ndarray) -> tuple[float, float, float, float, float, float]:
    """
    Raw (about the global origin, NOT centroidal) area and moments for a
    single closed polygon, via shoelace-formula polygon integration.

    Returns (A, Qx, Qy, Ixx_o, Iyy_o, Ixy_o) where:
        A      = signed area (positive if vertices are counter-clockwise)
        Qx     = first moment of area about the x-axis, i.e. integral of y dA
        Qy     = first moment of area about the y-axis, i.e. integral of x dA
        Ixx_o  = second moment about the x-axis through the origin
        Iyy_o  = second moment about the y-axis through the origin
        Ixy_o  = product of inertia about the origin
    """
    x = vertices[:, 0]
    y = vertices[:, 1]
    x1 = np.roll(x, -1)
    y1 = np.roll(y, -1)

    cross = x * y1 - x1 * y  # per-edge shoelace term

    A = np.sum(cross) / 2.0
    Qx = np.sum((y + y1) * cross) / 6.0
    Qy = np.sum((x + x1) * cross) / 6.0
    Ixx_o = np.sum((y**2 + y * y1 + y1**2) * cross) / 12.0
    Iyy_o = np.sum((x**2 + x * x1 + x1**2) * cross) / 12.0
    Ixy_o = np.sum((x * y1 + 2 * x * y + 2 * x1 * y1 + x1 * y) * cross) / 24.0

    return A, Qx, Qy, Ixx_o, Iyy_o, Ixy_o


def _perimeter(vertices: np.ndarray) -> float:
    x = vertices[:, 0]
    y = vertices[:, 1]
    x1 = np.roll(x, -1)
    y1 = np.roll(y, -1)
    return float(np.sum(np.hypot(x1 - x, y1 - y)))

# for MOI and section modulus calculations, we need the full set of properties

def compute_properties(shapes: list[np.ndarray]) -> SectionProperties:
    """
    Compute full section properties for a shape made of one or more
    closed polygons.

    `shapes` is a list of (N, 2) vertex arrays. Give solid regions in
    counter-clockwise order and holes in clockwise order (their signed
    area comes out negative automatically and is subtracted for you).
    A single solid shape is just `shapes=[vertices]`.
    """
    A_total = 0.0
    Qx_total = 0.0
    Qy_total = 0.0
    Ixx_o_total = 0.0
    Iyy_o_total = 0.0
    Ixy_o_total = 0.0
    perimeter_total = 0.0

    for verts in shapes:
        verts = np.asarray(verts, dtype=float)
        A, Qx, Qy, Ixx_o, Iyy_o, Ixy_o = _raw_moments(verts)
        A_total += A
        Qx_total += Qx
        Qy_total += Qy
        Ixx_o_total += Ixx_o
        Iyy_o_total += Iyy_o
        Ixy_o_total += Ixy_o
        perimeter_total += _perimeter(verts)

    if A_total <= 0:
        raise ValueError(
            "Total area came out zero or negative. Make sure solid outlines are "
            "counter-clockwise and holes are clockwise."
        )

    cx = Qy_total / A_total
    cy = Qx_total / A_total

    # Parallel axis theorem: shift from origin to the combined centroid
    Ixx = Ixx_o_total - A_total * cy**2
    Iyy = Iyy_o_total - A_total * cx**2
    Ixy = Ixy_o_total - A_total * cx * cy
    J = Ixx + Iyy

    # Principal moments of inertia (Mohr's circle for inertia)
    I_avg = (Ixx + Iyy) / 2.0
    R = np.sqrt(((Ixx - Iyy) / 2.0) ** 2 + Ixy**2)
    I_max = I_avg + R
    I_min = I_avg - R
    theta_p = 0.5 * np.degrees(np.arctan2(-2 * Ixy, Ixx - Iyy))

    rx = np.sqrt(Ixx / A_total)
    ry = np.sqrt(Iyy / A_total)

    all_x = np.concatenate([np.asarray(s)[:, 0] for s in shapes])
    all_y = np.concatenate([np.asarray(s)[:, 1] for s in shapes])

    c_top = float(np.max(all_y) - cy)
    c_bottom = float(cy - np.min(all_y))
    c_right = float(np.max(all_x) - cx)
    c_left = float(cx - np.min(all_x))

    def safe_div(a, b):
        return float(a / b) if b > 1e-15 else float("inf")

    return SectionProperties(
        area=A_total,
        centroid=(cx, cy),
        Ixx=Ixx,
        Iyy=Iyy,
        Ixy=Ixy,
        J=J,
        I_max=I_max,
        I_min=I_min,
        principal_angle_deg=theta_p,
        rx=rx,
        ry=ry,
        c_top=c_top,
        c_bottom=c_bottom,
        c_left=c_left,
        c_right=c_right,
        Sx_top=safe_div(Ixx, c_top),
        Sx_bottom=safe_div(Ixx, c_bottom),
        Sy_left=safe_div(Iyy, c_left),
        Sy_right=safe_div(Iyy, c_right),
        perimeter=perimeter_total,
        vertices=np.array(shapes, dtype=object),
    )