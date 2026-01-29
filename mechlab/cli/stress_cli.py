from mechlab.mechanics.stress import StressState
from mechlab.visual.stress_interactive import StressInteractive
from mechlab.visual.stress_export import StressAnimationExporter
from mechlab.export.csv_export import export_csv

def stress_compute(args):
    state = StressState(args.sx, args.sy, args.txy)
    results = state.results()

    for k, v in results.items():
        print(f"{k} = {v:.3f}")

    if args.csv:
        export_csv(results, args.csv)
        print(f"✔ CSV exported → {args.csv}")

def stress_show(args):
    gui = StressInteractive(args.sx, args.sy, args.txy)
    gui.show()

def stress_export(args):
    exporter = StressAnimationExporter(args.sx, args.sy, args.txy)

    if args.mp4:
        exporter.export_mp4(args.mp4)
    elif args.gif:
        exporter.export_gif(args.gif)
    else:
        print("❌ Choose --mp4 or --gif")
