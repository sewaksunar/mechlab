import numpy as np

def calculate_moment(force: float, distance: float) -> float:
    """
    Calculate the moment (torque) about a point.

    :param force: Applied force in Newtons (N).
    :param distance: Perpendicular distance from the pivot (m).
    :return: Moment in Newton-meters (Nm).
    """
    return float(force * distance)

def cantilever_deflection(P: float, L: float, E: float, I: float) -> float:
    """
    Calculate max deflection ($\delta$) for a cantilever beam with a point load at the end.

    .. math::
       \delta = \frac{P L^3}{3 E I}

    :param P: Load in Newtons (N).
    :param L: Length of beam (m).
    :param E: Modulus of Elasticity (Pa).
    :param I: Moment of Inertia (m^4).
    """
    return (P * L**3) / (3 * E * I)