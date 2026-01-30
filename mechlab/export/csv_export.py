"""CSV export utilities for analysis results."""

import csv


def export_csv(results, filename):
    """
    Export analysis results to CSV file.
    
    Args:
        results: Dictionary of result key-value pairs
        filename: Output CSV filename
    """
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for k, v in results.items():
            writer.writerow([k, v])
