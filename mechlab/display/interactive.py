import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RadioButtons
from mechlab.core.stress import StressState

def interactive_stress():
    fig, ax = plt.subplots()
    plt.subplots_adjust(left=0.3, bottom=0.35)

    unit = "MPa"
    state = StressState(100, 50, 25, unit)

    text = ax.text(0.05, 0.6, "", transform=ax.transAxes)
    ax.axis("off")

    ax_sx = plt.axes([0.3, 0.25, 0.6, 0.03])
    ax_sy = plt.axes([0.3, 0.20, 0.6, 0.03])
    ax_t  = plt.axes([0.3, 0.15, 0.6, 0.03])

    s_sx = Slider(ax_sx, 'σx', -500, 500, valinit=100)
    s_sy = Slider(ax_sy, 'σy', -500, 500, valinit=50)
    s_t  = Slider(ax_t,  'τxy', -500, 500, valinit=25)

    ax_unit = plt.axes([0.05, 0.4, 0.15, 0.25])
    unit_radio = RadioButtons(ax_unit, ("MPa", "GPa", "psi"))

    def update(val=None):
        nonlocal state, unit
        state = StressState(s_sx.val, s_sy.val, s_t.val, unit)
        r = state.results(unit)
        text.set_text(
            f"σ1 = {r['σ1']:.2f} {unit}\n"
            f"σ2 = {r['σ2']:.2f} {unit}\n"
            f"Von Mises = {r['von_mises']:.2f} {unit}"
        )
        fig.canvas.draw_idle()

    def unit_change(label):
        nonlocal unit
        unit = label
        update()

    for s in (s_sx, s_sy, s_t):
        s.on_changed(update)

    unit_radio.on_clicked(unit_change)

    update()
    plt.show()
