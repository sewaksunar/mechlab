"""Export utilities for CSV, PDF, and other formats."""

from .csv_export import export_csv

# Lazy-load PDF export to avoid hard dependency on reportlab
def __getattr__(name):
    if name == "export_pdf":
        from .pdf_export import export_pdf
        return export_pdf
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

__all__ = ["export_csv", "export_pdf"]
