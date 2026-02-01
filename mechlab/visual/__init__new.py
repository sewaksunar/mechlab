"""Visualization tools for engineering analysis.

Provides:
  - Matplotlib-based interactive viewers
  - Jupyter notebook widgets
  - Animation export (MP4/GIF)
  - Beam diagrams

Matplotlib visualizations:
  - StressViewer: Interactive stress analysis with sliders
  - BeamPlot: Shear force and bending moment diagrams

Jupyter widgets (requires ipywidgets):
  - stress_widget: Interactive stress widget for notebooks

Animation export:
  - StressAnimation: Export stress transformation to MP4/GIF
"""

from __future__ import annotations


# Lazy loading for faster imports
def __getattr__(name: str):
    _imports = {
        # Matplotlib viewers
        "StressViewer": "viewer",
        "BeamPlot": "beam",
        # Animation
        "StressAnimation": "animation",
        # Jupyter widgets
        "stress_widget": "widgets",
    }
    
    if name in _imports:
        module_name = _imports[name]
        module = __import__(f"mechlab.visual.{module_name}", fromlist=[name])
        return getattr(module, name)
    
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "StressViewer",
    "BeamPlot",
    "StressAnimation",
    "stress_widget",
]
