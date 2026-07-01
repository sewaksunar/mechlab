"""Tests for application.workflows — the design-check coordination layer."""

from mechlab.application.api import BeamAnalysis
from mechlab.application.config import AnalysisConfig
from mechlab.application.workflows import run_design_check
from mechlab.domain.entities import Material, Section


def _make_analysis(point_load: float) -> BeamAnalysis:
    steel = Material("steel", young_modulus=200e9, yield_strength=250e6)
    section = Section("I-beam", moment_of_inertia=9.19e-6, area=2.3e-3,
                       extreme_fiber_distance=0.076)
    return (
        BeamAnalysis(length=4.0, material=steel, section=section)
        .set_simple_supports(0.0, 4.0)
        .add_point_load(2.0, point_load)
    )


def test_design_check_passes_for_light_load():
    result = run_design_check(_make_analysis(point_load=1000))
    assert result.passed is True
    assert result.safety_factor > 1.5


def test_design_check_fails_for_heavy_load():
    config = AnalysisConfig(min_safety_factor=1.5)
    result = run_design_check(_make_analysis(point_load=500_000), config=config)
    assert result.passed is False
