from rich.console import Console
from rich.table import Table

from mechlab.units.registry import UNITS
from mechlab.units.convert import convert, UnitError

console = Console()


def run_units(args):
    if not args or args[0] == "list":
        _list_units()
        return

    if args[0] == "convert":
        _convert(args[1:])
        return

    console.print("[red]Unknown units command[/red]")


def _list_units():
    console.rule("[bold cyan]Supported Units")

    for category, units in UNITS.items():
        table = Table(title=category.capitalize())
        table.add_column("Unit")
        table.add_column("Factor to SI")

        for u, f in units.items():
            table.add_row(u, str(f))

        console.print(table)


def _convert(args):
    if len(args) != 3:
        console.print("[red]Usage: mechlab units convert <value> <from> <to>[/red]")
        return

    value, from_u, to_u = args

    try:
        value = float(value)
        result = convert(value, from_u, to_u)
        console.print(
            f"[green]{value} {from_u} = {result:.6g} {to_u}[/green]"
        )
    except ValueError:
        console.print("[red]Value must be numeric[/red]")
    except UnitError as e:
        console.print(f"[red]{e}[/red]")
