import argparse
from mechlab.cli.stress_cli import (
    stress_compute,
    stress_show,
    stress_export
)

def main():
    parser = argparse.ArgumentParser(
        prog="mechlab",
        description="MechLab – Mechanical Engineering Toolkit"
    )

    subparsers = parser.add_subparsers(dest="module")

    # ================= STRESS =================
    stress = subparsers.add_parser("stress", help="Stress analysis tools")
    stress_sub = stress.add_subparsers(dest="command")

    def add_common_args(p):
        p.add_argument("--sx", type=float, required=True)
        p.add_argument("--sy", type=float, required=True)
        p.add_argument("--txy", type=float, required=True)

    # compute
    compute = stress_sub.add_parser("compute", help="Compute stress values")
    add_common_args(compute)
    compute.add_argument("--csv", help="Export results to CSV")
    compute.set_defaults(func=stress_compute)

    # show
    show = stress_sub.add_parser("show", help="Interactive visualization")
    add_common_args(show)
    show.set_defaults(func=stress_show)

    # export
    export = stress_sub.add_parser("export", help="Export animation")
    add_common_args(export)
    export.add_argument("--mp4", help="Export MP4 file")
    export.add_argument("--gif", help="Export GIF file")
    export.set_defaults(func=stress_export)

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()
