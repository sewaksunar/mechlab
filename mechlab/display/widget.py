"""Jupyter widget-based display for stress analysis.

Requires: ipywidgets
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mechlab.mechanics.stress import StressState


def show_stress(state: "StressState") -> None:
    """
    Display interactive stress widget in Jupyter notebook.

    Args:
        state: StressState object with initial stress values

    Raises:
        RuntimeError: If ipywidgets is not available
    """
    try:
        import ipywidgets as w
        from IPython.display import display, clear_output
    except ImportError:
        raise RuntimeError(
            "ipywidgets not available. Install with: pip install ipywidgets"
        )

    from mechlab.mechanics.stress import StressState

    # Create sliders
    sx = w.FloatSlider(
        value=state.sigma_x,
        min=-500,
        max=500,
        step=1,
        description="σx (MPa)",
    )
    sy = w.FloatSlider(
        value=state.sigma_y,
        min=-500,
        max=500,
        step=1,
        description="σy (MPa)",
    )
    txy = w.FloatSlider(
        value=state.tau_xy,
        min=-500,
        max=500,
        step=1,
        description="τxy (MPa)",
    )

    out = w.Output()

    def update(change=None):
        with out:
            clear_output(wait=True)
            s = StressState(sx.value, sy.value, txy.value)
            s1, s2 = s.principal()
            print(f"σ1   = {s1:.2f} MPa")
            print(f"σ2   = {s2:.2f} MPa")
            print(f"τmax = {s.max_shear():.2f} MPa")
            print(f"VM   = {s.von_mises():.2f} MPa")

    for widget in (sx, sy, txy):
        widget.observe(update, "value")

    update()
    display(w.VBox([sx, sy, txy, out]))
