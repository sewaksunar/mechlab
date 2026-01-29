# mechlab/export/csv_export.py
import csv

def export_csv(results, filename):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for k, v in results.items():
            writer.writerow([k, v])
