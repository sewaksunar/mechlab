"""3D stress tensor transformations and principal stress calculations."""

import numpy as np
import sympy as sp


class StressTensor3D:
    """Represents a 3D stress tensor."""
    
    def __init__(self, components):
        """
        Initialize 3D stress tensor.
        
        Args:
            components: 3x3 matrix of stress components
            
        Raises:
            ValueError: If components is not a 3x3 matrix
        """
        if len(components) != 3 or any(len(row) != 3 for row in components):
            raise ValueError("Stress tensor must be a 3x3 matrix.")
        self.components = np.array(components)


class StressTransform:
    """Symbolic stress tensor transformation in 3D."""
    
    def __init__(self):
        """Initialize symbolic stress transformation matrices."""
        self.l1, self.m1, self.n1 = sp.symbols('l1 m1 n1')
        self.l2, self.m2, self.n2 = sp.symbols('l2 m2 n2')
        self.l3, self.m3, self.n3 = sp.symbols('l3 m3 n3')
        self.sxx, self.syy, self.szz = sp.symbols('sxx syy szz')
        self.sxy, self.syz, self.sxz = sp.symbols('sxy syz sxz')
        
        self.L = sp.Matrix([
            [self.l1, self.m1, self.n1],
            [self.l2, self.m2, self.n2],
            [self.l3, self.m3, self.n3]
        ])
        
        self.sigma = sp.Matrix([
            [self.sxx, self.sxy, self.sxz],
            [self.sxy, self.syy, self.syz],
            [self.sxz, self.syz, self.szz]
        ])
    
    def transform(self):
        """Compute transformed stress tensor: L * σ * L^T."""
        return self.L * self.sigma * self.L.T


class PrincipalStresses:
    """Calculate principal stresses from stress tensor."""
    
    @staticmethod
    def calculate(stress_tensor):
        """
        Calculate principal stresses (eigenvalues) sorted in descending order.
        
        Args:
            stress_tensor: 3x3 stress tensor
            
        Returns:
            List of principal stresses [σ1, σ2, σ3] where σ1 >= σ2 >= σ3
        """
        stress_matrix = np.array(stress_tensor)
        principal = np.linalg.eigvalsh(stress_matrix)
        return np.sort(principal)[::-1].tolist()