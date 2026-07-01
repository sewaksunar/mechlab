"""
Numerical/computation layer. Solvers know nothing about "beams" —
they operate on generic loads/supports handed to them. This keeps
domain classes decoupled from solving algorithms (Strategy pattern).
"""

from __future__ import annotations

from mechlab.domain.entities import Load, Support


class EquilibriumSolver:
    """
    Solves reactions for a simply-supported system with exactly two
    vertical supports (pin/roller) under vertical loads only.
    """

    def solve_two_support_reactions(
        self, length: float, loads: list[Load], supports: list[Support]
    ) -> None:
        if len(supports) != 2:
            raise ValueError("This solver requires exactly 2 supports")

        s1, s2 = sorted(supports, key=lambda s: s.position)
        total_load = sum(load.total_force() for load in loads)
        total_moment_about_s1 = sum(load.moment_about(s1.position) for load in loads)

        span = s2.position - s1.position
        if span <= 0:
            raise ValueError("Supports must be at distinct, ordered positions")

        # Sum of moments about s1 = 0  =>  R2 * span = total_moment_about_s1
        s2.reaction_force = total_moment_about_s1 / span
        # Sum of vertical forces = 0
        s1.reaction_force = total_load - s2.reaction_force
