import numpy as np
import sympy as sp

class StressTensor3D:
    def __init__(self, components):
        if len(components) != 3 or any(len(row) != 3 for row in components):
            raise ValueError("Stress tensor must be a 3x3 matrix.")
        self.components = np.array(components)

class StressTransform:
    """Symbolic stress tensor transformation in 3D."""
    def __init__(self):
        self.l1, self.m1, self.n1 = sp.symbols('l1 m1 n1')
        self.l2, self.m2, self.n2 = sp.symbols('l2 m2 n2')
        self.l3, self.m3, self.n3 = sp.symbols('l3 m3 n3')
        self.sxx, self.syy, self.szz = sp.symbols('sxx syy szz')
        self.sxy, self.syz, self.sxz = sp.symbols('sxy syz sxz')

        self.L = sp.Matrix([[self.l1, self.m1, self.n1], 
                            [self.l2, self.m2, self.n2], 
                            [self.l3, self.m3, self.n3]])
        
        self.sigma = sp.Matrix([[self.sxx, self.sxy, self.sxz],
                                [self.sxy, self.syy, self.syz],
                                [self.sxz, self.syz, self.szz]])

    def transform(self):
        return self.L * self.sigma * self.L.T

class PrincipalStresses:
    @staticmethod
    def calculate(stress_tensor):
        stress_matrix = np.array(stress_tensor)
        principal = np.linalg.eigvalsh(stress_matrix)
        return np.sort(principal)[::-1].tolist()