"""Visualization tools for engineering analysis.

Consolidated visual module providing:

Animation (use these):
  - animate(): Universal animation factory for ANY physics object
  - PhysicsAnimator: Generic animator for Animatable objects
  - Projection: 3D to 2D projection utilities
  - animate_cube(): Demo cube rotation animation

Stress Visualization:
  - StressViewer: Interactive viewer with Mohr's circle
  - StressAnimation: Export stress transformation to MP4/GIF

Beam Visualization:
  - BeamPlot: Shear force and bending moment diagrams

Jupyter Widgets:
  - stress_widget: Interactive stress widget for notebooks

Example:
    >>> from mechlab.mechanics.dynamics import Projectile
    >>> from mechlab.visual import animate
    >>> proj = Projectile(velocity=(20, 20, 0))
    >>> anim = animate(proj)
    >>> anim.preview()
    >>> anim.save_gif("projectile.gif")

Requires: matplotlib, numpy
Optional: ipywidgets (for Jupyter widgets), ffmpeg (for MP4 export)
"""

from __future__ import annotations


# Lazy loading for faster imports
def __getattr__(name: str):
    _imports = {
        # Universal animator (recommended)
        "animate": "animator",
        "PhysicsAnimator": "animator",
        "BaseAnimator": "animator",
        "Projection": "animator",
        "animate_cube": "animator",
        # Stress visualization (consolidated in viewer.py)
        "StressViewer": "viewer",
        "StressAnimation": "viewer",
        # Other visualization
        "BeamPlot": "beam",
        # Jupyter widgets
        "stress_widget": "widgets",
        # Legacy aliases (backward compatibility)
        "StressInteractive": "viewer",
        "StressRotationAnimation": "viewer",
        "StressAnimationExporter": "viewer",
        "StressGUI": "viewer",
        "ProjectileAnimation": "animator",  # → PhysicsAnimator
    }

    if name in _imports:
        module_name = _imports[name]
        module = __import__(f"mechlab.visual.{module_name}", fromlist=[name])

        # Handle legacy aliases → new class names
        if name in ("StressInteractive", "StressGUI"):
            return getattr(module, "StressViewer")
        if name in ("StressRotationAnimation", "StressAnimationExporter"):
            return getattr(module, "StressAnimation")
        if name == "ProjectileAnimation":
            return getattr(module, "PhysicsAnimator")

        return getattr(module, name)

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    # Universal (recommended)
    "animate",
    "PhysicsAnimator",
    "BaseAnimator",
    "Projection",
    "animate_cube",
    # Stress visualization
    "StressViewer",
    "StressAnimation",
    # Other
    "BeamPlot",
    "stress_widget",
    # Legacy aliases (deprecated, will be removed)
    "StressInteractive",
    "StressGUI",
    "ProjectileAnimation",
]
