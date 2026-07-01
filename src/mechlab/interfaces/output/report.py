"""
interfaces.output.report — formats analysis results for humans.

This module ONLY does presentation. It must never contain physics
or solving logic — if you find yourself computing a new value here
instead of formatting an existing one, that logic belongs in
domain/ or application/ instead.
"""

from __future__ import annotations

from typing import Any


class ReportGenerator:
    """Formats a BeamAnalysis.run() result dict into readable output."""

    def to_text(self, report: dict[str, Any]) -> str:
        """Render the report as a plain-text block.

        Args:
            report: the dict returned by BeamAnalysis.run().

        Returns:
            A multi-line human-readable string.
        """
        lines = ["=== Beam Analysis Report ===", ""]

        lines.append("Reactions:")
        for pos, force in report["reactions"]:
            lines.append(f"  x = {pos:.3f} m  ->  R = {force:.2f} N")

        lines.append("")
        stress_mpa = report["max_bending_stress_Pa"] / 1e6
        lines.append(f"Max bending stress : {stress_mpa:.2f} MPa "
                      f"at x = {report['max_bending_stress_location_m']:.2f} m")
        lines.append(f"Safety factor       : {report['safety_factor']:.2f}")

        return "\n".join(lines)

    def to_dict(self, report: dict[str, Any]) -> dict[str, Any]:
        """Pass-through for JSON/API consumers — kept for symmetry with to_text."""
        return report
