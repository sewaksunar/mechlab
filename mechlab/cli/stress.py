"""CLI commands for plane stress analysis.

Provides commands for:
  - Computing principal stresses and von Mises stress
  - Interactive stress visualization
  - Exporting animations (MP4/GIF)
"""

from __future__ import annotations

from mechlab.cli.common import get_flag, get_str, has_flag, print_error, print_success


def _show_help() -> None:
    """Display help for stress commands."""
    print("Stress Analysis Commands")
    print()
    print("Usage: mechlab stress <subcommand> --sx <val> --sy <val> --txy <val> [options]")
    print()
    print("Subcommands:")
    print("  compute   Calculate principal stresses, max shear, and von Mises")
    print("  show      Open interactive stress visualization window")
    print("  export    Export stress transformation animation")
    print()
    print("Required Arguments:")
    print("  --sx      Normal stress in x-direction (MPa)")
    print("  --sy      Normal stress in y-direction (MPa)")
    print("  --txy     Shear stress (MPa)")
    print()
    print("Options for 'compute':")
    print("  --csv <file>    Export results to CSV file")
    print()
    print("Options for 'export':")
    print("  --mp4 <file>    Export animation as MP4")
    print("  --gif <file>    Export animation as GIF")
    print()
    print("Examples:")
    print("  mechlab stress compute --sx 100 --sy 50 --txy 25")
    print("  mechlab stress compute --sx 100 --sy 50 --txy 25 --csv results.csv")
    print("  mechlab stress show --sx 100 --sy 50 --txy 25")
    print("  mechlab stress export --sx 100 --sy 50 --txy 25 --gif stress.gif")


def compute_stress(
    sx: float,
    sy: float,
    txy: float,
    csv_file: str | None = None,
) -> dict:
    """
    Compute and display stress analysis results.

    Args:
        sx: Normal stress in x-direction
        sy: Normal stress in y-direction
        txy: Shear stress
        csv_file: Optional path to export CSV

    Returns:
        Dictionary of computed results
    """
    from mechlab.mechanics.stress import StressState
    from mechlab.export.csv_export import export_csv

    state = StressState(sx, sy, txy)
    results = state.results()

    # Display results
    print()
    print("Stress Analysis Results")
    print("-" * 35)

    for key, value in results.items():
        if isinstance(value, (int, float)):
            print(f"  {key:>12} = {value:>12.3f}")
        elif value is not None:
            print(f"  {key:>12} = {value}")

    print()

    # Export if requested
    if csv_file:
        export_csv(results, csv_file)
        print_success(f"CSV exported to {csv_file}")

    return results


def show_stress(sx: float, sy: float, txy: float) -> None:
    """
    Display interactive stress visualization.

    Args:
        sx: Normal stress in x-direction
        sy: Normal stress in y-direction
        txy: Shear stress
    """
    from mechlab.visual.stress_interactive import StressInteractive

    gui = StressInteractive(sx, sy, txy)
    gui.show()


def export_stress(
    sx: float,
    sy: float,
    txy: float,
    mp4: str | None = None,
    gif: str | None = None,
) -> None:
    """
    Export stress animation to MP4 or GIF.

    Args:
        sx: Normal stress in x-direction
        sy: Normal stress in y-direction
        txy: Shear stress
        mp4: Output MP4 filename
        gif: Output GIF filename
    """
    from mechlab.visual.stress_export import StressAnimationExporter

    exporter = StressAnimationExporter(sx, sy, txy)

    if mp4:
        exporter.export_mp4(mp4)
    elif gif:
        exporter.export_gif(gif)
    else:
        print_error("Specify output format: --mp4 <file> or --gif <file>")


def run_stress(args: list[str]) -> None:
    """
    Execute stress analysis CLI command.

    Args:
        args: Command-line arguments
    """
    # Show help
    if not args or has_flag(args, "-h", "--help", "help"):
        _show_help()
        return

    subcommand, *rest = args

    # Parse required arguments
    sx = get_flag(rest, "--sx")
    sy = get_flag(rest, "--sy")
    txy = get_flag(rest, "--txy")

    # Validate inputs
    if sx is None or sy is None or txy is None:
        print_error("Missing required arguments: --sx, --sy, --txy")
        print()
        print("Example: mechlab stress compute --sx 100 --sy 50 --txy 25")
        return

    # Route to subcommand
    if subcommand == "compute":
        csv_file = get_str(rest, "--csv")
        compute_stress(sx, sy, txy, csv_file)

    elif subcommand == "show":
        show_stress(sx, sy, txy)

    elif subcommand == "export":
        mp4 = get_str(rest, "--mp4")
        gif = get_str(rest, "--gif")
        export_stress(sx, sy, txy, mp4=mp4, gif=gif)

    else:
        print_error(f"Unknown subcommand: {subcommand}")
        print()
        print("Available subcommands: compute, show, export")
        print("Run 'mechlab stress --help' for details.")
