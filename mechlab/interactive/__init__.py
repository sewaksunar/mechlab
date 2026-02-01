"""Jupyter notebook widgets for interactive analysis.

Provides interactive widgets for:
  - Stress state analysis
  - Real-time parameter adjustment

Requires: ipywidgets
"""

from __future__ import annotations


# Lazy-load widgets to avoid hard dependency on ipywidgets
def __getattr__(name: str):
    if name == "stress_state_widget":
        from .stress import stress_state_widget
        return stress_state_widget
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = ["stress_state_widget"]
