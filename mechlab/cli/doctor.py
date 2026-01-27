import sys
import json
import platform
import importlib.util
from typing import Dict

from rich.console import Console
from rich.table import Table

from mechlab import __version__

console = Console()


def _check_module(name: str) -> Dict[str, str]:
    spec = importlib.util.find_spec(name)
    if spec is None:
        return {"status": "missing"}
    module = __import__(name)
    version = getattr(module, "__version__", "unknown")
    return {"status": "ok", "version": version}


def _in_venv() -> bool:
    return sys.prefix != sys.base_prefix


def run_doctor(verbose: bool = False, json_mode: bool = False):
    report = {
        "mechlab_version": __version__,
        "python_version": sys.version.split()[0],
        "python_executable": sys.executable,
        "os": f"{platform.system()} {platform.release()}",
        "venv": _in_venv(),
        "dependencies": {},
        "warnings": [],
        "errors": [],
    }

    # Dependency checks
    required_deps = ["rich", "numpy"]
    for dep in required_deps:
        report["dependencies"][dep] = _check_module(dep)

        if report["dependencies"][dep]["status"] != "ok":
            report["errors"].append(f"Missing dependency: {dep}")

    # Python version warning
    py_major, py_minor = sys.version_info[:2]
    if py_major == 3 and py_minor < 9:
        report["warnings"].append("Python < 3.9 is not recommended")

    # JSON output
    if json_mode:
        print(json.dumps(report, indent=2))
        return

    # Rich output
    console.rule("[bold cyan]MechLab Doctor")

    table = Table(show_header=False, box=None)
    table.add_row("MechLab Version", report["mechlab_version"])
    table.add_row("Python", report["python_version"])
    table.add_row("OS", report["os"])
    table.add_row("Virtual Env", "Yes" if report["venv"] else "[yellow]No[/yellow]")

    if verbose:
        table.add_row("Python Exec", report["python_executable"])
        table.add_row("Prefix", sys.prefix)

    console.print(table)
    console.print()

    console.print("[bold]Dependencies[/bold]")
    for dep, info in report["dependencies"].items():
        if info["status"] == "ok":
            console.print(f"[green]✔ {dep}[/green] ({info['version']})")
        else:
            console.print(f"[red]✖ {dep}[/red]")

    if report["warnings"]:
        console.print("\n[yellow]Warnings[/yellow]")
        for w in report["warnings"]:
            console.print(f"[yellow]⚠ {w}[/yellow]")

    if report["errors"]:
        console.print("\n[red]Errors[/red]")
        for e in report["errors"]:
            console.print(f"[red]✖ {e}[/red]")
        console.print("\n[dim]Run: uv pip install -e .[/dim]")
    else:
        console.print("\n[green]✔ System looks healthy[/green]")
