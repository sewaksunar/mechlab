from mechlab.mechanics.stress import StressState
from mechlab.visual.stress_interactive import StressInteractive
from mechlab.visual.stress_export import StressAnimationExporter
from mechlab.export.csv_export import export_csv

def _get_flag(rest, name, default=None, cast=float):
    if name in rest:
        idx = rest.index(name)
        return cast(rest[idx + 1])
    return default

def _get_str(rest, name):
    if name in rest:
        idx = rest.index(name)
        return rest[idx + 1]
    return None

def run_stress(rest):
    if not rest:
        print("Usage: mechlab stress [compute|show|export]")
        return

    subcmd, *args = rest

    sx = _get_flag(args, "--sx")
    sy = _get_flag(args, "--sy")
    txy = _get_flag(args, "--txy")

    if sx is None or sy is None or txy is None:
        print("❌ Missing required arguments: --sx --sy --txy")
        return

    if subcmd == "compute":
        state = StressState(sx, sy, txy)
        results = state.results()

        for k, v in results.items():
            print(f"{k} = {v:.3f}")

        csv_file = _get_str(args, "--csv")
        if csv_file:
            export_csv(results, csv_file)
            print(f"✔ CSV exported → {csv_file}")

    elif subcmd == "show":
        gui = StressInteractive(sx, sy, txy)
        gui.show()

    elif subcmd == "export":
        exporter = StressAnimationExporter(sx, sy, txy)

        mp4 = _get_str(args, "--mp4")
        gif = _get_str(args, "--gif")

        if mp4:
            exporter.export_mp4(mp4)
        elif gif:
            exporter.export_gif(gif)
        else:
            print("❌ Use --mp4 <file> or --gif <file>")

    else:
        print(f"Unknown stress command: {subcmd}")
