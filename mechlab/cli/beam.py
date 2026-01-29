from mechlab.mechanics.beam import SimplySupportedBeam
from mechlab.visual.beam_plot import BeamPlot

def _get(rest, name, cast=float):
    if name in rest:
        i = rest.index(name)
        return cast(rest[i + 1])
    return None

def run_beam(rest):
    if not rest:
        print("Usage: mechlab beam [compute|show]")
        return

    cmd, *args = rest

    L = _get(args, "--L")
    P = _get(args, "--P")
    E = _get(args, "--E")
    I = _get(args, "--I")

    if None in (L, P, E, I):
        print("❌ Required: --L --P --E --I")
        return

    beam = SimplySupportedBeam(L, P, E, I)

    if cmd == "compute":
        for k, v in beam.results().items():
            print(f"{k}: {v:.6g}")

    elif cmd == "show":
        BeamPlot(beam).show()

    else:
        print(f"Unknown beam command: {cmd}")
