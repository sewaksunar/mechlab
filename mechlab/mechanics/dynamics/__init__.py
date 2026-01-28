r""""Dynamics of Particles"""
class DynamicsOfParticle:
    r"""
    Represents a particle in dynamics.
        .. math:: F = m a
    """
    def __init__(self, position, velocity, mass):
        self.position = position
        self.velocity = velocity
        self.mass = mass

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