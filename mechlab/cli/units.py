"""CLI commands for unit conversion.

Provides commands for:
  - Listing available units by category
  - Converting values between units
"""

from __future__ import annotations

from rich.console import Console
from rich.table import Table

from mechlab.units.registry import UNITS
from mechlab.units.convert import convert, UnitError

console = Console()


def _show_help() -> None:
    """Display help for units commands."""
    console.print("[bold]Unit Conversion Commands[/bold]")
    console.print()
    console.print("Usage: mechlab units <subcommand> [arguments]")
    console.print()
    console.print("Subcommands:")
    console.print("  list              List all available units")
    console.print("  convert <val> <from> <to>  Convert between units")
    console.print()
    console.print("Examples:")
    console.print("  mechlab units list")
    console.print("  mechlab units convert 100 MPa psi")
    console.print("  mechlab units convert 5 m ft")


def _list_units() -> None:
    """Display all available units organized by category."""
    console.rule("[bold cyan]Available Units")
    console.print()

    for category, units in UNITS.items():
        table = Table(
            title=f"[bold]{category.capitalize()}[/bold]",
            show_header=True,
            header_style="bold",
        )
        table.add_column("Unit", style="cyan")
        table.add_column("Factor to SI", justify="right")

        for unit, factor in sorted(units.items(), key=lambda x: x[1]):
            table.add_row(unit, f"{factor:g}")

        console.print(table)
        console.print()


def _convert(args: list[str]) -> None:
    """Convert a value from one unit to another."""
    if len(args) != 3:
        console.print("[red]Usage: mechlab units convert <value> <from> <to>[/red]")
        console.print()
        console.print("Example: mechlab units convert 100 MPa psi")
        return

    value_str, from_unit, to_unit = args

    try:
        value = float(value_str)
        result = convert(value, from_unit, to_unit)
        console.print(
            f"[green]{value:g} {from_unit} = {result:.6g} {to_unit}[/green]"
        )
    except ValueError:
        console.print("[red]Error: Value must be a number[/red]")
    except UnitError as e:
        console.print(f"[red]Error: {e}[/red]")


def run_units(args: list[str]) -> None:
    """
    Execute unit conversion CLI command.

    Args:
        args: Command-line arguments
    """
    # Show help
    if not args or args[0] in ("-h", "--help", "help"):
        _show_help()
        return

    subcommand, *rest = args

    if subcommand == "list":
        _list_units()
    elif subcommand == "convert":
        _convert(rest)
    else:
        console.print(f"[red]Unknown subcommand: {subcommand}[/red]")
        console.print()
        console.print("Run 'mechlab units --help' for available commands.")
