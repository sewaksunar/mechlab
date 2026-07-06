"""
Application layer: orchestrates domain + engine into user-friendly
workflows. This is the ONE place users should import from.
"""

from __future__ import annotations

from typing import Any

from mechlab.domain.entities import (
    DistributedLoad,
    Material,
    PointLoad,
    PointMoment,
    Section,
    Support,
    SupportType,
)
from mechlab.domain.strength.beam import Beam
from mechlab.interfaces.visual.plots import plot_fbd_beam, plot_moment, plot_shear


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

    def set_support(self, position: float, support_type: SupportType) -> BeamAnalysis:
        self.beam.add_support(Support(position, support_type))
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
    # free body diagram of beam
    def fbd_beam(
        self,
        save_path: str | None = None,
        show: bool = False,
    ) -> Any:
        """Solve the beam if needed and plot the free body diagram."""
        self.beam.solve()
        return plot_fbd_beam(self.beam, save_path=save_path, show=show)

    def plot_shear_moment(
        self,
        save_path: str | None = None,
        show: bool = False,
    ) -> Any:
        """Solve the beam if needed and plot the shear diagrams."""
        self.beam.solve()
        return plot_shear(self.beam, save_path=save_path, show=show)

    def plot_bending_moment_diagram(
        self,
        save_path: str | None = None,
        show: bool = False,
    ) -> Any:
        """Solve the beam if needed and plot the bending moment diagrams."""
        self.beam.solve()
        return plot_moment(self.beam, save_path=save_path, show=show)

    def add_moment(self, position: float, magnitude: float) -> BeamAnalysis:
        """
        Add a concentrated applied moment (couple) at a point.

        Sign convention: positive = counter-clockwise (N·m).
        """
        self.beam.add_load(PointMoment(position, magnitude))
        return self