r"""
Mechanics & Dynamics
====================

This module provides tools for both static structural analysis and 
rigid body dynamics.
"""

class Beam:
    r"""
    Represents a structural cantilever beam.

    **Deflection Formula:**

    .. math::

        \delta_{max} = \frac{P L^3}{3 E I}

    Args:
        L (float): Length [m].
        E (float): Young's Modulus [Pa].
        I (float): Moment of Inertia [m^4].
    """
    def __init__(self, L, E, I):
        self.L, self.E, self.I = L, E, I

    def max_deflection(self, load):
        r"""
        Calculates max deflection at the free end using:
        :math:`\delta = \frac{FL^3}{3EI}`
        """
        return (load * self.L**3) / (3 * self.E * self.I)



class RigidBody:
    r"""
    Represents a point mass for dynamic calculations.

    **Weight Calculation:**

    .. math::

        W = m \cdot g

    Args:
        mass (float): Mass [kg].
        position (tuple): (x, y) coordinates [m].
    """
    def __init__(self, mass, position):
        self.mass = mass
        self.position = position

    def weight(self):
        """Returns weight in Newtons (:math:`N`)."""
        return self.mass * 9.81