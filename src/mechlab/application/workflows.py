"""
application.workflows — multi-step analyses that go beyond a single
facade call: batch comparisons, design checks, what-if scenarios.
Anything that coordinates *multiple* BeamAnalysis runs belongs here,
keeping api.py focused on single-analysis convenience.
"""

from __future__ import annotations

from dataclasses import dataclass

from mechlab.application.api import BeamAnalysis
from mechlab.application.config import DEFAULT_CONFIG, AnalysisConfig


@dataclass
class DesignCheckResult:
    """Outcome of a single design check against a safety threshold.

    Attributes:
        passed: True if safety_factor >= config.min_safety_factor.
        safety_factor: the computed safety factor.
        report: the full underlying BeamAnalysis.run() report dict.
    """
    passed: bool
    safety_factor: float
    report: dict


def run_design_check(
    analysis: BeamAnalysis, config: AnalysisConfig = DEFAULT_CONFIG
) -> DesignCheckResult:
    """Run a beam analysis and evaluate it against a safety threshold.

    This is a workflow, not a domain calculation: it adds no new
    physics, only coordinates an existing BeamAnalysis run with an
    application-level pass/fail policy.

    Args:
        analysis: a configured (but not yet run) BeamAnalysis.
        config: thresholds to evaluate against. Defaults to DEFAULT_CONFIG.

    Returns:
        DesignCheckResult with pass/fail verdict and the full report.
    """
    report = analysis.run()
    safety_factor = report["safety_factor"]
    return DesignCheckResult(
        passed=safety_factor >= config.min_safety_factor,
        safety_factor=safety_factor,
        report=report,
    )
