"""Visualization and animation tools for engineering analysis.

Provides:
  - Beam diagrams (shear force, bending moment)
  - Stress transformation animations
  - Interactive stress viewers
  - Export to MP4/GIF

Requires: matplotlib, numpy
"""

from __future__ import annotations

# Lazy loading to speed up import
def __getattr__(name: str):
    lazy_imports = {
        "BeamPlot": "beam_plot",
        "StressRotationAnimation": "stress_animation",
        "StressAnimationExporter": "stress_export",
        "StressGUI": "stress_gui",
        "StressInteractive": "stress_interactive",
    }

    if name in lazy_imports:
        module_name = lazy_imports[name]
        module = __import__(f"mechlab.visual.{module_name}", fromlist=[name])
        return getattr(module, name)

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "BeamPlot",
    "StressRotationAnimation",
    "StressAnimationExporter",
    "StressGUI",
    "StressInteractive",
]
