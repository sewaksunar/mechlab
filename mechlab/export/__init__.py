"""Export utilities for CSV, PDF, and other formats.

Provides functions to export analysis results:
  - CSV: Simple tabular export
  - PDF: Formatted reports (requires reportlab)
"""

from __future__ import annotations

from .csv_export import export_csv, export_csv_table


# Lazy-load PDF export to avoid hard dependency on reportlab
def __getattr__(name: str):
    if name == "export_pdf":
        from .pdf_export import export_pdf
        return export_pdf
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = ["export_csv", "export_csv_table", "export_pdf"]
