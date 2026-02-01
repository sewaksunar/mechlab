"""Dynamics: motion analysis and rigid body dynamics.

Provides:
  - RigidBody: Point mass calculations
  - DynamicsOfParticle: Particle motion (position, velocity, mass)
"""

from __future__ import annotations


class DynamicsOfParticle:
    """
    Represents a particle in dynamics.
    
    Tracks position, velocity, and mass for kinematic calculations.
    
    Example:
        >>> p = DynamicsOfParticle(position=(0, 0, 0), velocity=(5, 0, 0), mass=10)
        >>> p.kinetic_energy()
        125.0
    """

    def __init__(
        self,
        position: tuple[float, float, float],
        velocity: tuple[float, float, float],
        mass: float,
    ) -> None:
        self.position = position
        self.velocity = velocity
        self.mass = mass

    def kinetic_energy(self) -> float:
        """Calculate kinetic energy: KE = ½mv²."""
        vx, vy, vz = self.velocity
        v_squared = vx**2 + vy**2 + vz**2
        return 0.5 * self.mass * v_squared


class RigidBody:
    """
    Represents a point mass for dynamic calculations.
    
    Example:
        >>> body = RigidBody(mass=10, position=(0, 0, 0))
        >>> body.weight()
        98.1
    """

    def __init__(
        self,
        mass: float,
        position: tuple[float, float, float],
    ) -> None:
        self.mass = mass
        self.position = position

    def weight(self, g: float = 9.81) -> float:
        """Calculate weight: W = mg."""
        return self.mass * g


__all__ = ["RigidBody", "DynamicsOfParticle"]