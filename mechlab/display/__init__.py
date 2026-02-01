"""Display utilities for text, LaTeX, and interactive visualizations.

Provides:
  - Text output for terminal/console
  - LaTeX rendering for Jupyter notebooks
  - Interactive widgets (requires ipywidgets)
"""

from __future__ import annotations

from .text import show_stress_text

# Lazy-load interactive components to avoid hard dependencies
def __getattr__(name: str):
    if name == "interactive_stress":
        from .interactive import interactive_stress
        return interactive_stress
    if name == "show_stress_widget":
        from .widget import show_stress
        return show_stress
    if name == "show_stress_latex":
        from .latex import show_stress
        return show_stress
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "show_stress_text",
    "interactive_stress",
    "show_stress_widget",
    "show_stress_latex",
]
