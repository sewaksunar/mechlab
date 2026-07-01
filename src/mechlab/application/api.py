"""
Application layer: orchestrates domain + engine into user-friendly
workflows. This is the ONE place users should import from.
"""

from __future__ import annotations

from mechlab.domain.entities import (
    DistributedLoad,
    Material,
    PointLoad,
    Section,
    Support,
    SupportType,
)
from mechlab.domain.strength.beam import Beam


class BeamAnalysis:
    """
    High-level facade wrapping Beam construction + solving + reporting,
    so a user doesn't have to touch domain/engine internals directly.
    """

    def __init__(self, length: float, material: Material, section: Section):
        self.beam = Beam(length, material, section)

    def add_point_load(self, position: float, magnitude: float) -> BeamAnalysis:
        self.beam.add_load(PointLoad(position, magnitude))
        return self

    def add_distributed_load(self, start: float, end: float, intensity: float) -> BeamAnalysis:
        self.beam.add_load(DistributedLoad(start, end, intensity))
        return self

    def set_simple_supports(self, pos_a: float, pos_b: float) -> BeamAnalysis:
        self.beam.add_support(Support(pos_a, SupportType.PIN))
        self.beam.add_support(Support(pos_b, SupportType.ROLLER))
        return self

    def run(self) -> dict:
        """Solve and return a summary report as a plain dict."""
        self.beam.solve()
        x_max, sigma_max = self.beam.max_bending_stress()
        yield_strength = self.beam.material.yield_strength
        return {
            "reactions": self.beam.reactions(),
            "max_bending_stress_Pa": sigma_max,
            "max_bending_stress_location_m": x_max,
            "safety_factor": yield_strength / sigma_max if sigma_max else float("inf"),
        }
