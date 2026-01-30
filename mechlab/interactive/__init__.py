"""Jupyter notebook widgets for interactive analysis."""

# Lazy-load stress widgets to avoid hard dependency on ipywidgets
def __getattr__(name):
    if name == "stress_state_widget":
        from .stress import stress_state_widget
        return stress_state_widget
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

__all__ = ["stress_state_widget"]
