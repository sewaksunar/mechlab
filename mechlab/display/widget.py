def show_stress(state):
    try:
        import ipywidgets as w
        from IPython.display import display, clear_output
    except ImportError:
        raise RuntimeError("ipywidgets not available")

    from mechlab.mechanics.stress import StressState

    sx = w.FloatSlider(value=state.sigma_x, min=-500, max=500, description="σx")
    sy = w.FloatSlider(value=state.sigma_y, min=-500, max=500, description="σy")
    t = w.FloatSlider(value=state.tau_xy, min=-500, max=500, description="τxy")

    out = w.Output()

    def update(change=None):
        with out:
            clear_output(wait=True)
            s = StressState(sx.value, sy.value, t.value)
            print(s)

    for wdg in (sx, sy, t):
        wdg.observe(update, "value")

    update()
    display(sx, sy, t, out)
