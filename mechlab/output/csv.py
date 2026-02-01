"""CSV export utilities for analysis results."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


def export_csv(
    results: dict[str, Any],
    filename: str | Path,
    include_header: bool = True,
) -> None:
    """
    Export analysis results to CSV file.

    Args:
        results: Dictionary of result key-value pairs
        filename: Output CSV filename or path
        include_header: Whether to include column headers

    Example:
        >>> results = {'σ1': 112.5, 'σ2': 37.5, 'unit': 'MPa'}
        >>> export_csv(results, 'stress_results.csv')
    """
    filepath = Path(filename)

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if include_header:
            writer.writerow(["Parameter", "Value"])

        for key, value in results.items():
            if isinstance(value, float):
                writer.writerow([key, f"{value:.6g}"])
            else:
                writer.writerow([key, value])


def export_csv_table(
    data: list[dict[str, Any]],
    filename: str | Path,
    fieldnames: list[str] | None = None,
) -> None:
    """
    Export list of dictionaries to CSV table.

    Args:
        data: List of dictionaries with consistent keys
        filename: Output CSV filename or path
        fieldnames: Column names (defaults to keys from first row)
    """
    if not data:
        return

    filepath = Path(filename)
    fields = fieldnames or list(data[0].keys())

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(data)
