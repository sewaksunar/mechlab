from typing import Union
import sympy as sp

Number = Union[int, float, sp.Expr]


class EngineeringBase:
    """
    Base class for all engineering objects.
    """

    def is_symbolic(self) -> bool:
        for v in self.__dict__.values():
            if isinstance(v, sp.Expr):
                return True
        return False

    def to_symbolic(self):
        raise NotImplementedError("Must implement to_symbolic()")
