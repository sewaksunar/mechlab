"""APPLICATION OF ENERGY METHODS IN MECHANICS"""

"""PRINCIPLE OF STATIONARY POTENTIAL ENERGY"""

class GeneralizedForce:
    def __init__(self, Q, q):
        self.Q = Q
        self.q = q
    def Qi(self):
        return self.Q * self.q
    
class CastiglianoFirstLaw:
    def __init__(self, generalized_force):
        self.generalized_force = generalized_force
    def stationary_potential_energy(self):
        
        return self.generalized_force.Qi() == 0