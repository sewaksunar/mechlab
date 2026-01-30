from mechlab.cli.common import get_flag
from mechlab.mechanics.beam import SimplySupportedBeam
from mechlab.visual.beam_plot import BeamPlot

def run_beam(rest):
    if not rest:
        print("Usage: mechlab beam [compute|show]")
        return

    cmd, *args = rest

    L = get_flag(args, "--L")
    P = get_flag(args, "--P")
    E = get_flag(args, "--E")
    I = get_flag(args, "--I")

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
