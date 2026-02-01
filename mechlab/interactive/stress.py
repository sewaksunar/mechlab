"""Interactive stress state widget for Jupyter notebooks.

Provides real-time stress analysis with slider controls.

Requires: ipywidgets
"""

from __future__ import annotations


def stress_state_widget(
    initial_sx: float = 100.0,
    initial_sy: float = 50.0,
    initial_txy: float = 25.0,
    value_range: tuple[float, float] = (-500, 500),
) -> None:
    """
    Display interactive widget for plane stress state analysis.

    Creates sliders for σx, σy, and τxy with real-time calculation
    of principal stresses, maximum shear, and von Mises stress.

    Args:
        initial_sx: Initial normal stress in x-direction (MPa)
        initial_sy: Initial normal stress in y-direction (MPa)
        initial_txy: Initial shear stress (MPa)
        value_range: Min/max range for sliders (default: -500 to 500)

    Raises:
        RuntimeError: If ipywidgets is not available

    Example:
        >>> from mechlab.interactive import stress_state_widget
        >>> stress_state_widget()  # In Jupyter notebook
    """
    try:
        import ipywidgets as w
        from IPython.display import display, clear_output
    except ImportError:
        raise RuntimeError(
            "ipywidgets not available. Install with: pip install ipywidgets"
        )

    from mechlab.mechanics.stress import StressState

    min_val, max_val = value_range

    # Input widgets
    sigma_x = w.FloatSlider(
        value=initial_sx,
        min=min_val,
        max=max_val,
        step=1,
        description="σx (MPa)",
        style={"description_width": "80px"},
    )

    sigma_y = w.FloatSlider(
        value=initial_sy,
        min=min_val,
        max=max_val,
        step=1,
        description="σy (MPa)",
        style={"description_width": "80px"},
    )

    tau_xy = w.FloatSlider(
        value=initial_txy,
        min=min_val,
        max=max_val,
        step=1,
        description="τxy (MPa)",
        style={"description_width": "80px"},
    )

    output = w.Output()

    def update(change=None):
        with output:
            clear_output(wait=True)

            state = StressState(
                sigma_x.value,
                sigma_y.value,
                tau_xy.value,
            )

            s1, s2 = state.principal_stresses()
            tmax = state.max_shear()
            vm = state.von_mises()

            print("Principal Stresses")
            print("-" * 25)
            print(f"σ₁ = {float(s1):>10.2f} MPa")
            print(f"σ₂ = {float(s2):>10.2f} MPa")
            print()
            print("Derived Values")
            print("-" * 25)
            print(f"τmax = {float(tmax):>8.2f} MPa")
            print(f"VM   = {float(vm):>8.2f} MPa")

    # Attach listeners
    sigma_x.observe(update, names="value")
    sigma_y.observe(update, names="value")
    tau_xy.observe(update, names="value")

    # Initial render
    update()

    # Display widget
    display(
        w.VBox(
            [
                w.HTML("<h4>Plane Stress Analysis</h4>"),
                sigma_x,
                sigma_y,
                tau_xy,
                w.HTML("<hr>"),
                output,
            ]
        )
    )
