"""Dynamics: motion analysis and rigid body dynamics.

Provides:
  - DynamicsOfParticle: Base particle motion (position, velocity, mass)
  - Projectile: Ballistic trajectory under gravity
  - RigidBody: Point mass calculations

All classes support the Animatable protocol for unified visualization.

Example:
    >>> from mechlab.mechanics.dynamics import Projectile
    >>> from mechlab.visual import animate
    >>> proj = Projectile(velocity=(20, 20, 0))
    >>> anim = animate(proj)  # Auto-creates appropriate animator
    >>> anim.preview()
"""

from __future__ import annotations

import math
from typing import Tuple, Optional, Dict, Any

import numpy as np
import sympy as sp

from mechlab.core.base import (
    PhysicsObject,
    PhysicsState,
    AnimatableMixin,
    ExportableMixin,
    physics_registry,
    Vector3D,
)


# =============================================================================
# BASE PARTICLE CLASS
# =============================================================================

class DynamicsOfParticle(PhysicsObject, AnimatableMixin, ExportableMixin):
    """Base class for particles in dynamics.

    Tracks position, velocity, and mass. Provides foundation for
    more specialized motion types (projectile, oscillator, etc.).

    Implements Animatable protocol for unified visualization.

    Example:
        >>> p = DynamicsOfParticle(position=(0, 0, 0), velocity=(5, 0, 0), mass=10)
        >>> p.kinetic_energy()
        125.0
        >>> p.speed
        5.0
    """

    def __init__(
        self,
        position: Vector3D = (0.0, 0.0, 0.0),
        velocity: Vector3D = (0.0, 0.0, 0.0),
        mass: float = 1.0,
    ) -> None:
        super().__init__(position=position, velocity=velocity, mass=mass)

    def state_at_time(self, t: float) -> PhysicsState:
        """Get state at time t (no acceleration for base particle)."""
        return PhysicsState(
            time=t,
            position=self.position,
            velocity=self.velocity,
            acceleration=(0.0, 0.0, 0.0),
        )

    def time_span(self) -> Tuple[float, float]:
        """Return default time span (0 to 1 second)."""
        return (0.0, 1.0)


# =============================================================================
# PROJECTILE CLASS
# =============================================================================

@physics_registry.register("projectile", category="dynamics", description="Ballistic motion under gravity")
class Projectile(DynamicsOfParticle):
    r"""Projectile motion under constant gravitational acceleration.

    Inherits from DynamicsOfParticle and extends with ballistic trajectory
    calculations. Fully compatible with the unified animation framework.

    Attributes:
        position: Initial position (x, y, z) in meters
        velocity: Initial velocity (vx, vy, vz) in m/s
        mass: Mass in kg
        g: Gravitational acceleration (default: 9.81 m/s²)

    Example:
        >>> proj = Projectile(velocity=(20, 20, 0), mass=1.0)
        >>> proj.time_of_flight()
        4.077
        >>> proj.max_height()
        20.39
        >>> proj.range()
        81.55

        # Animation
        >>> from mechlab.visual import animate
        >>> anim = animate(proj)
        >>> anim.preview()

    Physics:
        - Time of flight: $t = \frac{2v_y}{g}$
        - Range: $R = \frac{v_x \cdot 2v_y}{g}$
        - Max height: $h = \frac{v_y^2}{2g}$
        - Position: $\vec{r}(t) = \vec{r}_0 + \vec{v}_0 t - \frac{1}{2}g t^2 \hat{j}$
    """

    def __init__(
        self,
        position: Vector3D = (0.0, 0.0, 0.0),
        velocity: Vector3D = (0.0, 0.0, 0.0),
        mass: float = 1.0,
        g: float = 9.81,
    ) -> None:
        """Initialize projectile.

        Args:
            position: Initial position (x, y, z) in meters
            velocity: Initial velocity (vx, vy, vz) in m/s
            mass: Mass in kg
            g: Gravitational acceleration (default: 9.81 m/s²)
        """
        super().__init__(position=position, velocity=velocity, mass=mass)
        self.g = float(g)

    def time_of_flight(self) -> float:
        """Time until projectile returns to launch height.

        Returns:
            Time in seconds
        """
        _, vy, _ = self.velocity
        if vy <= 0:
            return 0.0
        return (2 * vy) / self.g

    def time_span(self) -> Tuple[float, float]:
        """Return valid time range for trajectory."""
        return (0.0, self.time_of_flight())

    def range(self) -> float:
        """Horizontal range of the projectile.

        Returns:
            Horizontal distance in meters
        """
        vx, vy, _ = self.velocity
        if vy <= 0:
            return 0.0
        return vx * self.time_of_flight()

    def max_height(self) -> float:
        """Maximum height above launch point.

        Returns:
            Height in meters
        """
        _, vy, _ = self.velocity
        if vy <= 0:
            return 0.0
        return (vy ** 2) / (2 * self.g)

    def state_at_time(self, t: float) -> PhysicsState:
        """Get complete physical state at time t.

        Args:
            t: Time in seconds

        Returns:
            PhysicsState with position, velocity, acceleration
        """
        pos = self.position_at_time(t)
        vel = self.velocity_at_time(t)

        return PhysicsState(
            time=t,
            position=pos,
            velocity=vel,
            acceleration=(0.0, -self.g, 0.0),
            energy={
                "kinetic": 0.5 * self.mass * sum(v**2 for v in vel),
                "potential": self.mass * self.g * pos[1],
            },
        )

    def position_at_time(self, t: float) -> Vector3D:
        """Position vector at time t.

        Args:
            t: Time in seconds

        Returns:
            Position (x, y, z) in meters
        """
        x0, y0, z0 = self.position
        vx, vy, vz = self.velocity
        return (
            x0 + vx * t,
            y0 + vy * t - 0.5 * self.g * t ** 2,
            z0 + vz * t,
        )

    def velocity_at_time(self, t: float) -> Vector3D:
        """Velocity vector at time t.

        Args:
            t: Time in seconds

        Returns:
            Velocity (vx, vy, vz) in m/s
        """
        vx, vy, vz = self.velocity
        return (vx, vy - self.g * t, vz)

    def trajectory(
        self,
        num_points: Optional[int] = None,
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Generate full trajectory arrays.

        Args:
            num_points: Number of points (default: 200)

        Returns:
            (t_array, positions[N,3], velocities[N,3])
        """
        n = num_points or self.DEFAULT_NUM_POINTS
        t_max = self.time_of_flight()

        if t_max <= 0:
            return (
                np.array([0.0]),
                np.array([self.position]),
                np.array([self.velocity]),
            )

        t_array = np.linspace(0, t_max, n)
        positions = np.array([self.position_at_time(t) for t in t_array])
        velocities = np.array([self.velocity_at_time(t) for t in t_array])

        return t_array, positions, velocities


# =============================================================================
# RIGID BODY CLASS
# =============================================================================

@physics_registry.register("rigid_body", category="dynamics", description="Point mass")
class RigidBody(PhysicsObject):
    """Point mass for basic dynamic calculations.

    Example:
        >>> body = RigidBody(mass=10, position=(0, 0, 0))
        >>> body.weight()
        98.1
    """

    def __init__(
        self,
        mass: float,
        position: Vector3D = (0.0, 0.0, 0.0),
        velocity: Vector3D = (0.0, 0.0, 0.0),
    ) -> None:
        super().__init__(position=position, velocity=velocity, mass=mass)

    def weight(self, g: float = 9.81) -> float:
        """Calculate weight: W = mg."""
        return self.mass * g

    def state_at_time(self, t: float) -> PhysicsState:
        """Static body - state doesn't change."""
        return PhysicsState(
            time=t,
            position=self.position,
            velocity=self.velocity,
            acceleration=(0.0, 0.0, 0.0),
        )

    def time_span(self) -> Tuple[float, float]:
        return (0.0, 1.0)


__all__ = ["DynamicsOfParticle", "Projectile", "RigidBody"]