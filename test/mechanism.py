from mechlab.core.stress import StressState
from mechlab.export.csv_export import export_csv
from mechlab.export.pdf_export import export_pdf

s = StressState(100, 50, 25, unit="MPa")
results = s.results("MPa")

export_csv(results, "stress_test.csv")
export_pdf(results, "stress_test.pdf")

print("Export done")
