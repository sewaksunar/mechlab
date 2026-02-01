"""Text-based display utilities for stress analysis.

Provides formatted console output for stress calculations.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mechlab.mechanics.stress import StressState


def show_stress_text(state: "StressState", precision: int = 2) -> None:
    """
    Display stress analysis results in formatted text.

    Args:
        state: StressState object with stress values
        precision: Number of decimal places (default: 2)

    Example:
        >>> from mechlab.mechanics.stress import StressState
        >>> state = StressState(100, 50, 25)
        >>> show_stress_text(state)

        Stress Analysis Results
        --------------------------------
        σx   = 100.00 MPa
        σy   = 50.00 MPa
        τxy  = 25.00 MPa
        σ1   = 112.50 MPa
        σ2   = 37.50 MPa
        τmax = 37.50 MPa
        VM   = 97.43 MPa
    """
    s1, s2 = state.principal()
    unit = state.unit or ""
    unit_suffix = f" {unit}" if unit else ""

    print()
    print("Stress Analysis Results")
    print("-" * 35)
    print(f"  σx   = {state.sx:.{precision}f}{unit_suffix}")
    print(f"  σy   = {state.sy:.{precision}f}{unit_suffix}")
    print(f"  τxy  = {state.txy:.{precision}f}{unit_suffix}")
    print(f"  σ1   = {s1:.{precision}f}{unit_suffix}")
    print(f"  σ2   = {s2:.{precision}f}{unit_suffix}")
    print(f"  τmax = {state.max_shear():.{precision}f}{unit_suffix}")
    print(f"  VM   = {state.von_mises():.{precision}f}{unit_suffix}")
    print()
