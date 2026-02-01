"""Simply supported beam analysis.

Provides calculations for:
  - Reaction forces
  - Maximum bending moment
  - Maximum deflection
"""

from __future__ import annotations


class SimplySupportedBeam:
    """
    Simply supported beam with center point load.

    Calculates reactions, maximum moment, and maximum deflection
    for a beam with a concentrated load at the center.

    Attributes:
        L: Beam length (m)
        P: Point load at center (N)
        E: Young's modulus (Pa)
        I: Second moment of area (m^4)
        RA: Reaction at support A (N)
        RB: Reaction at support B (N)
        M_max: Maximum bending moment (N·m)
        delta_max: Maximum deflection (m)

    Example:
        >>> beam = SimplySupportedBeam(5, 1000, 200e9, 1e-4)
        >>> beam.M_max
        1250.0
    """

    def __init__(
        self,
        length: float,
        load: float,
        E: float,
        I: float,
    ) -> None:
        """
        Initialize simply supported beam.

        Args:
            length: Beam length (m)
            load: Point load at center (N)
            E: Young's modulus (Pa)
            I: Second moment of area (m^4)

        Raises:
            ValueError: If any parameter is non-positive
        """
        if length <= 0:
            raise ValueError("Length must be positive")
        if E <= 0:
            raise ValueError("Young's modulus must be positive")
        if I <= 0:
            raise ValueError("Second moment of area must be positive")

        self.L = float(length)
        self.P = float(load)
        self.E = float(E)
        self.I = float(I)

        self._compute()

    def _compute(self) -> None:
        """Compute beam analysis results."""
        # Reactions (symmetric for center load)
        self.RA = self.P / 2
        self.RB = self.P / 2

        # Maximum moment at center
        self.M_max = self.P * self.L / 4

        # Maximum deflection at center
        self.delta_max = (self.P * self.L**3) / (48 * self.E * self.I)

    def results(self) -> dict[str, float]:
        """
        Return analysis results as dictionary.

        Returns:
            Dictionary with all computed values
        """
        return {
            "Length (L)": self.L,
            "Load (P)": self.P,
            "Young's Modulus (E)": self.E,
            "Moment of Inertia (I)": self.I,
            "Reaction A (RA)": self.RA,
            "Reaction B (RB)": self.RB,
            "Max Moment (M_max)": self.M_max,
            "Max Deflection (δ_max)": self.delta_max,
        }

    def __repr__(self) -> str:
        return (
            f"SimplySupportedBeam(L={self.L}, P={self.P}, "
            f"E={self.E:.2e}, I={self.I:.2e})"
        )
