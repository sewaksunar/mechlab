"""Statics: equilibrium analysis of rigid bodies and structures."""

import sympy as sp
from sympy.vector import CoordSys3D

r""""Statics of Particles"""
class StaticsParticle:
    r"""
    Represents a particle in statics.
        .. math:: F = F1 + F2 + ... + Fn
    """
    def __init__(self, forces): # forces is sympy vector
        self.forces = forces # list of forces acting on the particle
        self.v1 = sp.Matrix(forces[0][:])
        self.v2 = sp.Matrix(forces[1][:])
    def resultant(self):
        self.resultant = self.v1 + self.v2
        return self.resultant
    def inclination(self):
        r"""
        Calculates the inclination angle of the resultant force.
            .. math:: \theta = \tan^{-1}\left(\frac{F_y}{F_x}\right)
        """
        Fx, Fy, Fz = self.resultant
        theta_xy = sp.atan2(Fy, Fx)
        theta_xz = sp.atan2(Fz, Fx)
        theta_yz = sp.atan2(Fz, Fy)
        return theta_xy, theta_xz, theta_yz
    
    def resolve_components(self):
        r"""
        Resolves the resultant force into its components along the coordinate axes.
            .. math:: F_x = F \cos(\theta_x)
            .. math:: F_y = F \cos(\theta_y)
            .. math:: F_z = F \cos(\theta_z)
        """
        Fx, Fy, Fz = self.resultant
        magnitude = sp.sqrt(Fx**2 + Fy**2 + Fz**2)
        theta_x = sp.acos(Fx / magnitude)
        theta_y = sp.acos(Fy / magnitude)
        theta_z = sp.acos(Fz / magnitude)
        return (magnitude * sp.cos(theta_x),
                magnitude * sp.cos(theta_y),
                magnitude * sp.cos(theta_z))
    
    def unit_vector(self):
        r"""
        Calculates the unit vector in the direction of the resultant force.
            .. math:: \hat{F} = \frac{F}{|F|}
        """
        Fx, Fy, Fz = self.resultant
        magnitude = sp.sqrt(Fx**2 + Fy**2 + Fz**2)
        return (Fx / magnitude, Fy / magnitude, Fz / magnitude)

class Beam:
    r"""
    Represents a structural cantilever beam.
        .. math:: \delta_{max} = \frac{P L^3}{3 E I}
    """
    def __init__(self, L, E, I):
        self.L, self.E, self.I = L, E, I

    def max_deflection(self, load):
        return (load * self.L**3) / (3 * self.E * self.I)

    def slope(self, x):
        return x**2