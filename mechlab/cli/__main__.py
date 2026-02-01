"""Main CLI entry point for MechLab.

This module provides the primary command-line interface for MechLab,
routing commands to their respective handlers.
"""

from __future__ import annotations

import sys
from typing import NoReturn

from mechlab import __version__

# Command handlers (imported lazily for faster startup)
COMMANDS = {
    "doctor": "mechlab.cli.doctor:run_doctor",
    "shell": "mechlab.cli.shell:run_shell",
    "units": "mechlab.cli.units:run_units",
    "math": "mechlab.cli.math:run_math",
    "stress": "mechlab.cli.stress:run_stress",
    "beam": "mechlab.cli.beam:run_beam",
}


def _import_handler(path: str):
    """Lazily import a command handler from module path."""
    module_path, func_name = path.split(":")
    module = __import__(module_path, fromlist=[func_name])
    return getattr(module, func_name)


def _show_help() -> None:
    """Display help message with available commands."""
    print(f"MechLab v{__version__} - Mechanical Engineering Laboratory")
    print()
    print("Usage: mechlab <command> [options]")
    print()
    print("Commands:")
    print("  shell     Interactive Python shell with MechLab preloaded")
    print("  stress    Plane stress analysis (compute, show, export)")
    print("  beam      Beam analysis (compute, show)")
    print("  units     Unit conversion and listing")
    print("  math      Basic engineering calculations")
    print("  doctor    Check system dependencies and health")
    print()
    print("Options:")
    print("  -h, --help     Show this help message")
    print("  -v, --version  Show version number")
    print()
    print("Examples:")
    print("  mechlab stress compute --sx 100 --sy 50 --txy 25")
    print("  mechlab beam compute --L 5 --P 1000 --E 200e9 --I 1e-4")
    print("  mechlab units convert 100 MPa psi")


def _show_version() -> None:
    """Display version information."""
    print(f"MechLab v{__version__}")


def main() -> None:
    """Main CLI entry point."""
    args = sys.argv[1:]

    # No arguments -> interactive shell
    if not args:
        handler = _import_handler(COMMANDS["shell"])
        handler()
        return

    cmd, *rest = args

    # Handle global flags
    if cmd in ("-h", "--help", "help"):
        _show_help()
        return

    if cmd in ("-v", "--version", "version"):
        _show_version()
        return

    # Route to command handler
    if cmd in COMMANDS:
        handler = _import_handler(COMMANDS[cmd])

        # Special handling for doctor command flags
        if cmd == "doctor":
            handler(
                verbose="--verbose" in rest or "-v" in rest,
                json_mode="--json" in rest,
            )
        else:
            handler(rest)
    else:
        print(f"Error: Unknown command '{cmd}'")
        print()
        print("Run 'mechlab --help' for available commands.")
        sys.exit(1)


if __name__ == "__main__":
    main()
