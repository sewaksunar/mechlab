"""CLI commands for beam analysis.

Provides commands for:
  - Computing beam reactions, moments, and deflections
  - Visualizing shear force and bending moment diagrams
"""

from __future__ import annotations

from mechlab.cli.common import get_flag, has_flag, print_error


def _show_help() -> None:
    """Display help for beam commands."""
    print("Beam Analysis Commands")
    print()
    print("Usage: mechlab beam <subcommand> --L <val> --P <val> --E <val> --I <val>")
    print()
    print("Subcommands:")
    print("  compute   Calculate reactions, moments, and max deflection")
    print("  show      Display shear and moment diagrams")
    print()
    print("Required Arguments:")
    print("  --L       Beam length (m)")
    print("  --P       Point load at center (N)")
    print("  --E       Young's modulus (Pa)")
    print("  --I       Second moment of area (m^4)")
    print()
    print("Examples:")
    print("  mechlab beam compute --L 5 --P 1000 --E 200e9 --I 1e-4")
    print("  mechlab beam show --L 5 --P 1000 --E 200e9 --I 1e-4")


def run_beam(args: list[str]) -> None:
    """
    Execute beam analysis CLI command.

    Args:
        args: Command-line arguments
    """
    # Show help
    if not args or has_flag(args, "-h", "--help", "help"):
        _show_help()
        return

    subcommand, *rest = args

    # Parse required arguments
    L = get_flag(rest, "--L")
    P = get_flag(rest, "--P")
    E = get_flag(rest, "--E")
    I = get_flag(rest, "--I")

    # Validate inputs
    if None in (L, P, E, I):
        print_error("Missing required arguments: --L, --P, --E, --I")
        print()
        print("Example: mechlab beam compute --L 5 --P 1000 --E 200e9 --I 1e-4")
        return

    # Lazy import to speed up CLI startup
    from mechlab.mechanics.beam import SimplySupportedBeam

    beam = SimplySupportedBeam(L, P, E, I)

    # Route to subcommand
    if subcommand == "compute":
        print()
        print("Simply Supported Beam Analysis")
        print("-" * 40)

        results = beam.results()
        for key, value in results.items():
            print(f"  {key:<20} = {value:>12.6g}")

        print()

    elif subcommand == "show":
        from mechlab.visual.beam_plot import BeamPlot
        BeamPlot(beam).show()

    else:
        print_error(f"Unknown subcommand: {subcommand}")
        print()
        print("Available subcommands: compute, show")
        print("Run 'mechlab beam --help' for details.")
