"""Visualization tools for engineering analysis.

Provides:
  - StressViewer: Interactive stress analysis with Mohr's circle
  - BeamPlot: Shear force and bending moment diagrams
  - StressAnimation: Export stress transformation animations
  - stress_widget: Jupyter notebook widget for stress analysis

Requires: matplotlib, numpy
Optional: ipywidgets (for Jupyter widgets)
"""

from __future__ import annotations


# Lazy loading for faster imports
def __getattr__(name: str):
    _imports = {
        # Main classes
        "StressViewer": "viewer",
        "BeamPlot": "beam",
        "StressAnimation": "animation",
        # Jupyter widgets
        "stress_widget": "widgets",
        # Legacy aliases (backward compatibility)
        "StressInteractive": "viewer",
        "StressRotationAnimation": "animation",
        "StressAnimationExporter": "animation",
        "StressGUI": "viewer",
    }

    if name in _imports:
        module_name = _imports[name]
        module = __import__(f"mechlab.visual.{module_name}", fromlist=[name])
        
        # Handle legacy aliases → new class names
        if name in ("StressInteractive", "StressGUI"):
            return getattr(module, "StressViewer")
        if name in ("StressRotationAnimation", "StressAnimationExporter"):
            return getattr(module, "StressAnimation")
        
        return getattr(module, name)

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    # New consolidated classes
    "StressViewer",
    "BeamPlot",
    "StressAnimation",
    "stress_widget",
    # Legacy aliases (deprecated)
    "StressInteractive",
    "StressGUI",
    "StressRotationAnimation",
    "StressAnimationExporter",
]
