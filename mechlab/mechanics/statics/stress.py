"""3D stress tensor transformations and principal stress calculations.

Provides:
  - StressTensor3D: 3D stress tensor representation
  - StressTransform: Symbolic stress tensor transformation
  - PrincipalStresses: Principal stress calculation from tensor
"""

from __future__ import annotations

import numpy as np
import sympy as sp


class StressTensor3D:
    """
    Represents a 3D stress tensor.
    
    The stress tensor is a symmetric 3x3 matrix:
        [[σxx, τxy, τxz],
         [τxy, σyy, τyz],
         [τxz, τyz, σzz]]
    
    Example:
        >>> tensor = StressTensor3D([[100, 25, 0], [25, 50, 0], [0, 0, 0]])
        >>> tensor.components
        array([[100,  25,   0],
               [ 25,  50,   0],
               [  0,   0,   0]])
    """

    def __init__(self, components: list[list[float]]) -> None:
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

    def trace(self) -> float:
        """Return the trace (sum of diagonal elements)."""
        return float(np.trace(self.components))

    def hydrostatic(self) -> float:
        """Return hydrostatic stress: σ_h = (σxx + σyy + σzz) / 3."""
        return self.trace() / 3


class StressTransform:
    """
    Symbolic stress tensor transformation in 3D.
    
    Uses direction cosines (l, m, n) to transform stress tensor
    from one coordinate system to another.
    
    Example:
        >>> transform = StressTransform()
        >>> result = transform.transform()  # Returns symbolic L * σ * L^T
    """

    def __init__(self) -> None:
        """Initialize symbolic stress transformation matrices."""
        # Direction cosines
        self.l1, self.m1, self.n1 = sp.symbols('l1 m1 n1')
        self.l2, self.m2, self.n2 = sp.symbols('l2 m2 n2')
        self.l3, self.m3, self.n3 = sp.symbols('l3 m3 n3')

        # Stress components
        self.sxx, self.syy, self.szz = sp.symbols('sxx syy szz')
        self.sxy, self.syz, self.sxz = sp.symbols('sxy syz sxz')

        # Transformation matrix
        self.L = sp.Matrix([
            [self.l1, self.m1, self.n1],
            [self.l2, self.m2, self.n2],
            [self.l3, self.m3, self.n3]
        ])

        # Stress tensor
        self.sigma = sp.Matrix([
            [self.sxx, self.sxy, self.sxz],
            [self.sxy, self.syy, self.syz],
            [self.sxz, self.syz, self.szz]
        ])

    def transform(self) -> sp.Matrix:
        """Compute transformed stress tensor: σ' = L * σ * L^T."""
        return self.L * self.sigma * self.L.T


class PrincipalStresses:
    """
    Calculate principal stresses from stress tensor.
    
    Principal stresses are the eigenvalues of the stress tensor,
    representing normal stresses on planes with no shear stress.
    
    Example:
        >>> tensor = [[100, 25, 0], [25, 50, 0], [0, 0, 0]]
        >>> PrincipalStresses.calculate(tensor)
        [110.355..., 39.644..., 0.0]
    """

    @staticmethod
    def calculate(stress_tensor: list[list[float]]) -> list[float]:
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


__all__ = ["StressTensor3D", "StressTransform", "PrincipalStresses"]