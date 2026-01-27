class RigidBody:
    r"""
    Represents a point mass for dynamic calculations.
        .. math:: W = m \cdot g
    """
    def __init__(self, mass, position):
        self.mass = mass
        self.position = position

    def weight(self):
        return self.mass * 9.81