# mechlab/interactive/stress_widget.py
import ipywidgets as w
from IPython.display import display

def stress_state_widget(state):
    sx = w.FloatSlider(value=state.sx, min=-500, max=500, description="σx")
    sy = w.FloatSlider(value=state.sy, min=-500, max=500, description="σy")
    txy = w.FloatSlider(value=state.txy, min=-500, max=500, description="τxy")

    output = w.Output()

    def update(*args):
        state.sx, state.sy, state.txy = sx.value, sy.value, txy.value
        with output:
            output.clear_output()
            for k, v in state.summary().items():
                print(f"{k:>4} : {v}")

    for s in (sx, sy, txy):
        s.observe(update, names="value")

    update()
    display(w.VBox([sx, sy, txy, output]))
