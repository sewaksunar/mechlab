"""Dynamics: motion analysis and rigid body dynamics.

Provides:
  - RigidBody: Point mass calculations
  - DynamicsOfParticle: Particle motion (position, velocity, mass)
"""

from __future__ import annotations
import math
import numpy as np
import sympy as sp

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

class Projectile:
    r"""Represents a projectile in motion.
    Tracks position, velocity, mass, and computes trajectory under gravity.
    Example:
        >>> proj = Projectile(position=(0, 0, 0), velocity=(10, 10, 0), mass=2)
        >>> proj.time_of_flight()
        2.0408163265306123
    Formulae used:
        - Time of flight: ..math: \( t = \frac{2v_0 \sin(\theta)}{g} \)
        - Range: ..math: \( R = \frac{v_0^2 \sin(2\theta)}{g} \)
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
        self.g = 9.81  # Acceleration due to gravity (m/s²)
    
    def x_displacement(self) -> float:
        """Calculate horizontal displacement."""
        vx, _, _ = self.velocity
        t_flight = self.time_of_flight()
        return vx * t_flight
    
    def y_displacement(self) -> float:
        """Calculate vertical displacement."""
        _, vy, _ = self.velocity
        t_flight = self.time_of_flight()
        return vy * t_flight - 0.5 * self.g * t_flight**2

    def time_of_flight(self) -> float:
        """Calculate time of flight until projectile lands back to initial height."""
        vx, vy, vz = self.velocity
        v0 = (vx**2 + vy**2 + vz**2)**0.5
        theta = math.asin(vy / v0)
        return (2 * v0 * math.sin(theta)) / self.g
    
    def range(self) -> float:
        """Calculate horizontal range of the projectile."""
        vx, vy, vz = self.velocity
        v0 = (vx**2 + vy**2 + vz**2)**0.5
        theta = math.asin(vy / v0)
        return (v0**2 * math.sin(2 * theta)) / self.g
    
    def position_at_time(self, t: float) -> tuple[float, float, float]:
        """Calculate position at time t."""
        x0, y0, z0 = self.position
        vx, vy, vz = self.velocity
        x_t = x0 + vx * t
        y_t = y0 + vy * t - 0.5 * self.g * t**2
        z_t = z0 + vz * t
        return (x_t, y_t, z_t)
    
    def velocity_at_time(self, t: float) -> tuple[float, float, float]:
        """Calculate velocity at time t."""
        vx, vy, vz = self.velocity
        vy_t = vy - self.g * t
        return (vx, vy_t, vz)

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


__all__ = ["RigidBody", "DynamicsOfParticle", "Projectile"]