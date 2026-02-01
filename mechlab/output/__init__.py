"""Output utilities for exporting and displaying results.

Provides:
  - Text output for terminal/console
  - CSV export for data files
  - PDF export for reports (requires reportlab)

Example:
    >>> from mechlab.output import print_stress, export_csv
    >>> print_stress(state)
    >>> export_csv(results, 'results.csv')
"""

from __future__ import annotations

from .text import print_stress, print_beam, print_results
from .csv import export_csv, export_csv_table


# Lazy-load PDF export to avoid hard dependency on reportlab
def __getattr__(name: str):
    if name == "export_pdf":
        from .pdf import export_pdf
        return export_pdf
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "print_stress",
    "print_beam", 
    "print_results",
    "export_csv",
    "export_csv_table",
    "export_pdf",
]
