import ipywidgets as w
from IPython.display import display, clear_output

from mechlab.mechanics.stress import StressState


def stress_state_widget():
    """Interactive widget for plane stress state."""

    # Input widgets
    sigma_x = w.FloatSlider(
        value=100,
        min=-500,
        max=500,
        step=10,
        description="σx (MPa)"
    )

    sigma_y = w.FloatSlider(
        value=50,
        min=-500,
        max=500,
        step=10,
        description="σy (MPa)"
    )

    tau_xy = w.FloatSlider(
        value=25,
        min=-500,
        max=500,
        step=10,
        description="τxy (MPa)"
    )

    output = w.Output()

    def update(change=None):
        with output:
            clear_output(wait=True)

            state = StressState(
                sigma_x.value,
                sigma_y.value,
                tau_xy.value
            )

            s1, s2 = state.principal_stresses()
            tmax = state.max_shear()

            print("Principal Stresses:")
            print(f"σ₁ = {float(s1):.2f} MPa")
            print(f"σ₂ = {float(s2):.2f} MPa")
            print(f"\nMax Shear Stress = {float(tmax):.2f} MPa")

    # Attach listeners
    sigma_x.observe(update, names="value")
    sigma_y.observe(update, names="value")
    tau_xy.observe(update, names="value")

    # Initial render
    update()

    display(
        w.VBox([
            sigma_x,
            sigma_y,
            tau_xy,
            output
        ])
    )
