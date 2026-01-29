import csv

def export_csv(results, filename):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        for k, v in results.items():
            writer.writerow([k, v])
