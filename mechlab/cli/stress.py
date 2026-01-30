"""CLI commands for stress analysis."""

from mechlab.cli.common import get_flag, get_str
from mechlab.mechanics.stress import StressState
from mechlab.visual.stress_interactive import StressInteractive
from mechlab.visual.stress_export import StressAnimationExporter
from mechlab.export.csv_export import export_csv


def compute_stress(sx, sy, txy, csv_file=None):
    """Compute and display stress analysis results."""
    state = StressState(sx, sy, txy)
    results = state.results()

    for k, v in results.items():
        if isinstance(v, (int, float)):
            print(f"{k} = {v:.3f}")
        else:
            print(f"{k} = {v}")

    if csv_file:
        export_csv(results, csv_file)
        print(f"✔ CSV exported → {csv_file}")

    return results


def show_stress(sx, sy, txy):
    """Display interactive stress visualization."""
    gui = StressInteractive(sx, sy, txy)
    gui.show()


def export_stress(sx, sy, txy, mp4=None, gif=None):
    """Export stress animation to MP4 or GIF."""
    exporter = StressAnimationExporter(sx, sy, txy)

    if mp4:
        exporter.export_mp4(mp4)
    elif gif:
        exporter.export_gif(gif)
    else:
        print("❌ Use --mp4 <file> or --gif <file>")


def run_stress(rest):
    if not rest:
        print("Usage: mechlab stress [compute|show|export]")
        return

    subcmd, *args = rest

    sx = get_flag(args, "--sx")
    sy = get_flag(args, "--sy")
    txy = get_flag(args, "--txy")

    if sx is None or sy is None or txy is None:
        print("❌ Missing required arguments: --sx --sy --txy")
        return

    if subcmd == "compute":
        csv_file = get_str(args, "--csv")
        compute_stress(sx, sy, txy, csv_file)
    elif subcmd == "show":
        show_stress(sx, sy, txy)
    elif subcmd == "export":
        mp4 = get_str(args, "--mp4")
        gif = get_str(args, "--gif")
        export_stress(sx, sy, txy, mp4=mp4, gif=gif)
    else:
        print(f"Unknown stress command: {subcmd}")
