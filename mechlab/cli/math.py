"""CLI commands for mathematical calculations."""

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


def run_math(args):
    """Execute math calculation command."""
    if not args or args[0] == "list":
        _list_math()
        return

    cmd, *rest = args

    try:
        if cmd == "stress":
            _calc(rest, stress, "Stress (σ)", "Pa")
        elif cmd == "strain":
            _calc(rest, strain, "Strain (ε)", "")
        elif cmd == "young":
            _calc(rest, youngs_modulus, "Young's Modulus (E)", "Pa")
        elif cmd == "pressure":
            _calc(rest, pressure, "Pressure (P)", "Pa")
        else:
            console.print("[red]Unknown math command[/red]")
    except MathError as e:
        console.print(f"[red]{e}[/red]")


def _calc(args, func, label, unit):
    if len(args) != 2:
        console.print("[red]Expected two numeric arguments[/red]")
        return

    try:
        a, b = map(float, args)
        result = func(a, b)
        suffix = f" {unit}" if unit else ""
        console.print(f"[green]{label}: {result:.6g}{suffix}[/green]")
    except ValueError:
        console.print("[red]Arguments must be numbers[/red]")


def _list_math():
    table = Table(title="MechLab Math Functions")
    table.add_column("Command")
    table.add_column("Formula")

    table.add_row("stress", "σ = F / A")
    table.add_row("strain", "ε = ΔL / L")
    table.add_row("young", "E = σ / ε")
    table.add_row("pressure", "P = F / A")

    console.print(table)
