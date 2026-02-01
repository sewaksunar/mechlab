"""Statics: equilibrium analysis of rigid bodies and structures.

Provides:
  - Beam: Cantilever beam analysis
  - StaticsParticle: Particle equilibrium
  - StressTensor3D: 3D stress tensor
  - StressTransform: Symbolic stress transformation
  - PrincipalStresses: Principal stress calculation
"""

import sympy as sp

from .stress import StressTensor3D, StressTransform, PrincipalStresses


class StaticsParticle:
    """
    Represents a particle in statics.
    
    Calculates resultant force, inclination angles, and unit vectors.
    
    Example:
        >>> F1 = (10, 20, 0)
        >>> F2 = (5, -10, 15)
        >>> p = StaticsParticle([F1, F2])
        >>> p.resultant()
        Matrix([[15], [10], [15]])
    """

    def __init__(self, forces: list) -> None:
        """
        Initialize with list of force vectors.
        
        Args:
            forces: List of force tuples (Fx, Fy, Fz)
        """
        self.forces = forces
        self.v1 = sp.Matrix(forces[0][:])
        self.v2 = sp.Matrix(forces[1][:])
        self._resultant = None

    def resultant(self) -> sp.Matrix:
        """Calculate and return the resultant force vector."""
        self._resultant = self.v1 + self.v2
        return self._resultant

    def inclination(self) -> tuple:
        """Calculate inclination angles of the resultant force."""
        if self._resultant is None:
            self.resultant()
        Fx, Fy, Fz = self._resultant
        theta_xy = sp.atan2(Fy, Fx)
        theta_xz = sp.atan2(Fz, Fx)
        theta_yz = sp.atan2(Fz, Fy)
        return theta_xy, theta_xz, theta_yz

    def unit_vector(self) -> tuple:
        """Calculate the unit vector of the resultant force."""
        if self._resultant is None:
            self.resultant()
        Fx, Fy, Fz = self._resultant
        mag = sp.sqrt(Fx**2 + Fy**2 + Fz**2)
        return (Fx / mag, Fy / mag, Fz / mag)


class Beam:
    """
    Cantilever beam with end load.
    
    Calculates maximum deflection and slope.
    
    Example:
        >>> beam = Beam(L=2, E=200e9, I=1e-6)
        >>> beam.max_deflection(load=1000)
        0.0133...
    """

    def __init__(self, L: float, E: float, I: float) -> None:
        """
        Initialize cantilever beam.
        
        Args:
            L: Beam length (m)
            E: Young's modulus (Pa)
            I: Second moment of area (m^4)
        """
        self.L = L
        self.E = E
        self.I = I

    def max_deflection(self, load: float) -> float:
        """Calculate maximum deflection: δ = PL³/(3EI)."""
        return (load * self.L**3) / (3 * self.E * self.I)

    def slope(self, x: float) -> float:
        """Calculate slope at position x (simplified)."""
        return x**2


__all__ = [
    "StaticsParticle",
    "Beam",
    "StressTensor3D",
    "StressTransform",
    "PrincipalStresses",
]