from mechlab.core.stress import StressState
from mechlab.display.interactive import interactive_stress
from mechlab.export.csv_export import export_csv
from mechlab.export.pdf_export import export_pdf

def stress(sx, sy, txy, unit="MPa", mode="text", export=None):
    state = StressState(sx, sy, txy, unit)

    if mode == "interactive":
        interactive_stress()
        return

    results = state.results(unit)

    for k, v in results.items():
        print(f"{k:>10} : {v}")

    if export == "csv":
        export_csv(results, "stress.csv")
    elif export == "pdf":
        export_pdf(results, "stress.pdf")
