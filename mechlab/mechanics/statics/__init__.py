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