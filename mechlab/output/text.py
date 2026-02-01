"""Text output utilities for displaying analysis results.

Provides formatted console output for engineering calculations.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from mechlab.mechanics.stress import StressState
    from mechlab.mechanics.beam import SimplySupportedBeam


def print_results(
    results: dict[str, Any],
    title: str = "Results",
    precision: int = 6,
) -> None:
    """
    Print a results dictionary in formatted table.

    Args:
        results: Dictionary of result key-value pairs
        title: Title to display above results
        precision: Number of significant figures for floats
    """
    print()
    print(title)
    print("-" * 40)
    
    for key, value in results.items():
        if isinstance(value, float):
            print(f"  {key:<24} = {value:>{precision}g}")
        elif value is not None:
            print(f"  {key:<24} = {value}")
    
    print()


def print_stress(state: "StressState", precision: int = 2) -> None:
    """
    Print stress analysis results in formatted text.

    Args:
        state: StressState object with stress values
        precision: Number of decimal places

    Example:
        >>> from mechlab.mechanics.stress import StressState
        >>> state = StressState(100, 50, 25)
        >>> print_stress(state)
    """
    s1, s2 = state.principal()
    unit = state.unit or ""
    suffix = f" {unit}" if unit else ""

    print()
    print("Stress Analysis Results")
    print("-" * 40)
    print(f"  σx   = {state.sx:>{precision+6}.{precision}f}{suffix}")
    print(f"  σy   = {state.sy:>{precision+6}.{precision}f}{suffix}")
    print(f"  τxy  = {state.txy:>{precision+6}.{precision}f}{suffix}")
    print(f"  σ1   = {s1:>{precision+6}.{precision}f}{suffix}")
    print(f"  σ2   = {s2:>{precision+6}.{precision}f}{suffix}")
    print(f"  τmax = {state.max_shear():>{precision+6}.{precision}f}{suffix}")
    print(f"  VM   = {state.von_mises():>{precision+6}.{precision}f}{suffix}")
    print()


def print_beam(beam: "SimplySupportedBeam", precision: int = 4) -> None:
    """
    Print beam analysis results in formatted text.

    Args:
        beam: SimplySupportedBeam object
        precision: Number of significant figures
    """
    print()
    print("Beam Analysis Results")
    print("-" * 40)
    print(f"  Length (L)      = {beam.L:>{precision}g} m")
    print(f"  Load (P)        = {beam.P:>{precision}g} N")
    print(f"  Reaction A      = {beam.RA:>{precision}g} N")
    print(f"  Reaction B      = {beam.RB:>{precision}g} N")
    print(f"  Max Moment      = {beam.M_max:>{precision}g} N·m")
    print(f"  Max Deflection  = {beam.delta_max:>{precision}g} m")
    print()
