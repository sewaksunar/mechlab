"""
application.config — application-level settings: tolerances, defaults,
numerical precision used across workflows. Not physical constants
(those belong in domain/engine) — this is *how the app behaves*,
not *what the physics says*.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AnalysisConfig:
    """Default settings for analysis workflows.

    Attributes:
        stress_sample_points: number of points used when scanning a
            beam for maximum bending stress. Higher = more accurate,
            slower. Passed through to Beam.max_bending_stress().
        min_safety_factor: threshold below which BeamAnalysis.run()
            results are considered a design failure by convention
            (informational only — mechlab does not enforce this).
    """
    stress_sample_points: int = 200
    min_safety_factor: float = 1.5


DEFAULT_CONFIG = AnalysisConfig()
