"""High-level API for MechLab.

This module provides a simplified interface for common operations,
suitable for quick calculations and scripts.

Example:
    >>> from mechlab.api import stress
    >>> stress(100, 50, 25)  # Quick stress analysis
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from mechlab.mechanics.stress import StressState


def stress(
    sx: float,
    sy: float,
    txy: float,
    unit: str = "MPa",
    mode: Literal["text", "interactive"] = "text",
    export: Literal["csv", "pdf"] | None = None,
) -> dict | None:
    """
    Perform plane stress analysis.

    Args:
        sx: Normal stress in x-direction
        sy: Normal stress in y-direction
        txy: Shear stress
        unit: Stress unit (default: MPa)
        mode: Display mode - 'text' or 'interactive'
        export: Export format - 'csv', 'pdf', or None

    Returns:
        Results dictionary (when mode='text'), None (when mode='interactive')

    Example:
        >>> results = stress(100, 50, 25)
        >>> results['σ1']  # Principal stress 1
        112.5
    """
    from mechlab.mechanics.stress import StressState

    state = StressState(sx, sy, txy, unit)

    if mode == "interactive":
        from mechlab.visual import StressViewer
        viewer = StressViewer(sx, sy, txy, unit)
        viewer.show()
        return None

    results = state.results(unit)

    # Display results
    from mechlab.output import print_stress
    print_stress(state)

    # Export if requested
    if export == "csv":
        from mechlab.output import export_csv
        export_csv(results, "stress_results.csv")
        print("✔ Exported to stress_results.csv")
    elif export == "pdf":
        from mechlab.output import export_pdf
        export_pdf(results, "stress_results.pdf")
        print("✔ Exported to stress_results.pdf")

    return results
