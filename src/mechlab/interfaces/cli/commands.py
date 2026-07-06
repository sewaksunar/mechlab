"""interfaces.cli.commands — command-line entry point.

Usage::

        python -m mechlab beam \\
            --length 4.0 \\
            --E 200e9 \\
            --yield 250e6 \\
            --I 9.19e-6 \\
            --area 2.3e-3 \\
            --c 0.076 \\
            --support 0.0 \\
            --support 4.0 \\
            --point-load 2.0 5000

This module only parses args and calls into `application/` — it
must never construct domain objects (Beam, Material, ...) directly
from raw CLI strings without going through the application facade,
so behavior stays identical whether triggered by CLI, script, or API.
"""

from __future__ import annotations

import argparse

from mechlab.application.api import BeamAnalysis
from mechlab.domain.entities import Material, Section
from mechlab.interfaces.output.report import ReportGenerator


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="mechlab", description="mechlab CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    beam = sub.add_parser("beam", help="Analyze a simply-supported beam")
    beam.add_argument("--length", type=float, required=True, help="Beam length (m)")
    beam.add_argument("--E", type=float, required=True, help="Young's modulus (Pa)")
    beam.add_argument("--yield", dest="yield_strength", type=float, required=True,
                       help="Material yield strength (Pa)")
    beam.add_argument("--I", type=float, required=True, help="Moment of inertia (m^4)")
    beam.add_argument("--area", type=float, required=True, help="Cross-sectional area (m^2)")
    beam.add_argument("--c", type=float, required=True, help="Extreme fiber distance (m)")
    beam.add_argument("--support", type=float, action="append", required=True,
                       help="Support position (m). Pass twice for pin+roller.")
    beam.add_argument("--point-load", type=float, nargs=2, action="append", default=[],
                       metavar=("POSITION", "MAGNITUDE"), help="Point load: position magnitude")

    return parser


def run_beam_command(args: argparse.Namespace) -> str:
    """Executes the 'beam' subcommand and returns a formatted report string."""
    if len(args.support) != 2:
        raise SystemExit("Exactly two --support values are required")

    material = Material(name="user-material", young_modulus=args.E,
                         yield_strength=args.yield_strength)
    section = Section(name="user-section", moment_of_inertia=args.I,
                       area=args.area, extreme_fiber_distance=args.c)

    analysis = BeamAnalysis(length=args.length, material=material, section=section)
    analysis.set_simple_supports(args.support[0], args.support[1])
    for position, magnitude in args.point_load:
        analysis.add_point_load(position, magnitude)

    result = analysis.run()
    return ReportGenerator().to_text(result)


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "beam":
        print(run_beam_command(args))
