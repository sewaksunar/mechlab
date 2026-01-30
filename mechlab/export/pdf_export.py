"""PDF export utilities for analysis results."""

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def export_pdf(results, filename):
    """
    Export analysis results to PDF file.
    
    Args:
        results: Dictionary of result key-value pairs
        filename: Output PDF filename
    """
    c = canvas.Canvas(filename, pagesize=A4)
    text = c.beginText(50, 800)
    
    text.setFont("Helvetica", 12)
    text.textLine("Stress Analysis Report")
    text.textLine("-" * 40)
    
    for k, v in results.items():
        text.textLine(f"{k} : {v}")
    
    c.drawText(text)
    c.showPage()
    c.save()
