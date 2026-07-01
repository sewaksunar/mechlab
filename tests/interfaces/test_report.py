"""Tests for interfaces.output.report — presentation layer only."""

from mechlab.interfaces.output.report import ReportGenerator


def _sample_report():
    return {
        "reactions": [(0.0, 2500.0), (4.0, 2500.0)],
        "max_bending_stress_Pa": 41_350_000.0,
        "max_bending_stress_location_m": 2.0,
        "safety_factor": 6.05,
    }


def test_to_text_includes_reactions():
    text = ReportGenerator().to_text(_sample_report())
    assert "x = 0.000 m" in text
    assert "x = 4.000 m" in text
    assert "R = 2500.00 N" in text


def test_to_text_includes_stress_and_safety_factor():
    text = ReportGenerator().to_text(_sample_report())
    assert "41.35 MPa" in text
    assert "6.05" in text


def test_to_dict_is_passthrough():
    report = _sample_report()
    assert ReportGenerator().to_dict(report) == report
