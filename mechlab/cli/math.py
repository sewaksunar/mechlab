"""CLI commands for basic engineering calculations.

Provides commands for:
  - Stress calculation (σ = F / A)
  - Strain calculation (ε = ΔL / L)
  - Young's modulus (E = σ / ε)
  - Pressure calculation (P = F / A)
"""

from __future__ import annotations

from rich.console import Console
from rich.table import Table

from mechlab.math.core import (
    stress,
    strain,
    youngs_modulus,
    pressure,
    MathError,
)

console = Console()


def _show_help() -> None:
    """Display help for math commands."""
    console.print("[bold]Engineering Math Commands[/bold]")
    console.print()
    console.print("Usage: mechlab math <function> <arg1> <arg2>")
    console.print()
    console.print("Functions:")
    _list_functions()
    console.print()
    console.print("Examples:")
    console.print("  mechlab math stress 1000 0.01    # σ = F/A = 1000/0.01")
    console.print("  mechlab math strain 0.5 100      # ε = ΔL/L = 0.5/100")
    console.print("  mechlab math young 200e6 0.001   # E = σ/ε")


def _list_functions() -> None:
    """Display available math functions."""
    table = Table(
        title="Available Functions",
        show_header=True,
        header_style="bold",
    )
    table.add_column("Command", style="cyan")
    table.add_column("Formula")
    table.add_column("Unit")

    table.add_row("stress", "σ = F / A", "Pa")
    table.add_row("strain", "ε = ΔL / L", "(dimensionless)")
    table.add_row("young", "E = σ / ε", "Pa")
    table.add_row("pressure", "P = F / A", "Pa")

    console.print(table)


def _calculate(
    args: list[str],
    func,
    label: str,
    unit: str,
) -> None:
    """
    Perform calculation and display result.

    Args:
        args: Two numeric arguments
        func: Calculation function
        label: Result label
        unit: Result unit
    """
    if len(args) != 2:
        console.print("[red]Error: Expected two numeric arguments[/red]")
        console.print()
        console.print("Example: mechlab math stress 1000 0.01")
        return

    try:
        a, b = map(float, args)
        result = func(a, b)
        suffix = f" {unit}" if unit else ""
        console.print(f"[green]{label}: {result:.6g}{suffix}[/green]")
    except ValueError:
        console.print("[red]Error: Arguments must be numbers[/red]")
    except MathError as e:
        console.print(f"[red]Error: {e}[/red]")


def run_math(args: list[str]) -> None:
    """
    Execute math calculation CLI command.

    Args:
        args: Command-line arguments
    """
    # Show help or list functions
    if not args or args[0] in ("-h", "--help", "help", "list"):
        _show_help()
        return

    command, *rest = args

    # Route to calculation function
    calculations = {
        "stress": (stress, "Stress (σ)", "Pa"),
        "strain": (strain, "Strain (ε)", ""),
        "young": (youngs_modulus, "Young's Modulus (E)", "Pa"),
        "pressure": (pressure, "Pressure (P)", "Pa"),
    }

    if command in calculations:
        func, label, unit = calculations[command]
        _calculate(rest, func, label, unit)
    else:
        console.print(f"[red]Unknown function: {command}[/red]")
        console.print()
        console.print("Run 'mechlab math --help' for available functions.")
