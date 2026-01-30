"""Base classes for engineering calculations."""

from typing import Union
import sympy as sp

Number = Union[int, float, sp.Expr]


class EngineeringBase:
    """Base class for all engineering objects with symbolic support."""
    
    def is_symbolic(self) -> bool:
        """
        Check if any attributes contain symbolic expressions.
        
        Returns:
            True if object contains symbolic expressions, False otherwise
        """
        for v in self.__dict__.values():
            if isinstance(v, sp.Expr):
                return True
        return False
    
    def to_symbolic(self):
        """Convert object to symbolic representation. Must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement to_symbolic()")
