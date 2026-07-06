"""
Beam: a concrete domain entity that inherits from Body. Demonstrates
OOP inheritance + delegation to an engine-layer solver (composition
over inheritance for the solving algorithm itself).
"""

from __future__ import annotations

from mechlab.domain.entities import Body, Material, Section, PointMoment
from mechlab.engine.math.solvers import MatrixBeamSolver


class Beam(Body):
    """A simply-supported beam under point/distributed vertical loads."""

    def __init__(self, length: float, material: Material, section: Section):
        super().__init__(length, material, section)
        self._solver = MatrixBeamSolver()
        self._solved = False

    def solve(self) -> None:
        """Compute support reactions using the matrix beam solver."""
        self._solver.solve(
            self.length, self.loads, self.supports
        )
        self._solved = True

    def _require_solved(self) -> None:
        if not self._solved:
            raise RuntimeError("Call beam.solve() before requesting results")

    def shear_at(self, x: float) -> float:
        """Internal shear force at position x (from the left end)."""
        self._require_solved()
        v = 0.0
        for s in self.supports:
            if s.position <= x:
                v += s.reaction_force
        for load in self.loads:
            if load.position <= x:
                v -= load.total_force()
        return v

    def moment_at(self, x: float) -> float:
        """Internal bending moment at position x (from the left end)."""
        self._require_solved()
        m = 0.0
        for s in self.supports:
            if s.position <= x:
                m += s.reaction_force * (x - s.position)
        for load in self.loads:
            if load.position <= x:
                m -= load.total_force() * (x - load.position)
        return m

    def max_bending_stress(self, num_points: int = 200) -> tuple[float, float]:
        """Returns (position, stress) of maximum absolute bending stress."""
        self._require_solved()
        z = self.section.section_modulus()
        best_x, best_stress = 0.0, 0.0
        for i in range(num_points + 1):
            x = self.length * i / num_points
            stress = abs(self.moment_at(x)) / z
            if stress > best_stress:
                best_x, best_stress = x, stress
        return best_x, best_stress

    def reactions(self) -> list[tuple[float, float]]:
        self._require_solved()
        return [(s.position, s.reaction_force) for s in self.supports]

    def __repr__(self) -> str:
        return f"Beam(length={self.length}m, material={self.material.name})"
    
    def moment_at(self, x: float) -> float:
        """Internal bending moment at position x (from the left end)."""
        self._require_solved()
        m = 0.0
        for s in self.supports:
            if s.position <= x:
                m += s.reaction_force * (x - s.position)
        for load in self.loads:
            if load.position <= x:
                if isinstance(load, PointMoment):
                    m += load.magnitude
                else:
                    m -= load.total_force() * (x - load.position)
        return m
