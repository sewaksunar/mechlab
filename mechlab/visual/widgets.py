"""Jupyter notebook widgets for interactive analysis.

Requires: ipywidgets
"""

from __future__ import annotations


def stress_widget(
    initial_sx: float = 100.0,
    initial_sy: float = 50.0,
    initial_txy: float = 25.0,
) -> None:
    """
    Display interactive stress widget in Jupyter notebook.

    Creates sliders for σx, σy, and τxy with real-time calculation
    of principal stresses, maximum shear, and von Mises stress.

    Args:
        initial_sx: Initial normal stress in x-direction (MPa)
        initial_sy: Initial normal stress in y-direction (MPa)
        initial_txy: Initial shear stress (MPa)

    Raises:
        RuntimeError: If ipywidgets is not available

    Example:
        >>> from mechlab.visual import stress_widget
        >>> stress_widget()  # In Jupyter notebook
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
        value=initial_sx,
        min=-500,
        max=500,
        step=1,
        description="σx (MPa)",
        style={"description_width": "80px"},
        layout=w.Layout(width="400px"),
    )
    sy = w.FloatSlider(
        value=initial_sy,
        min=-500,
        max=500,
        step=1,
        description="σy (MPa)",
        style={"description_width": "80px"},
        layout=w.Layout(width="400px"),
    )
    txy = w.FloatSlider(
        value=initial_txy,
        min=-500,
        max=500,
        step=1,
        description="τxy (MPa)",
        style={"description_width": "80px"},
        layout=w.Layout(width="400px"),
    )

    output = w.Output()

    def update(change=None):
        with output:
            clear_output(wait=True)
            
            state = StressState(sx.value, sy.value, txy.value)
            s1, s2 = state.principal()
            
            print("─" * 30)
            print("Principal Stresses")
            print("─" * 30)
            print(f"  σ₁   = {s1:>10.2f} MPa")
            print(f"  σ₂   = {s2:>10.2f} MPa")
            print()
            print("Derived Values")
            print("─" * 30)
            print(f"  τmax = {state.max_shear():>10.2f} MPa")
            print(f"  σvm  = {state.von_mises():>10.2f} MPa")

    # Attach listeners
    for slider in (sx, sy, txy):
        slider.observe(update, names="value")

    # Initial render
    update()

    # Display
    display(
        w.VBox([
            w.HTML("<h3>Plane Stress Analysis</h3>"),
            sx, sy, txy,
            w.HTML("<hr>"),
            output,
        ])
    )
