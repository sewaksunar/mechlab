"""
interfaces.visual.plots — shear/moment diagram plotting.

Requires matplotlib, which is an optional dependency (install with
`pip install mechlab[plots]` or `uv sync --extra plots`) so that core
mechlab usage never forces a plotting dependency on users who only
need numeric results (e.g. running in a headless service).
"""

from __future__ import annotations

from mechlab.domain.strength.beam import Beam


def plot_shear_moment(beam: Beam, num_points: int = 200):
    """Plot shear force and bending moment diagrams for a solved beam.

    Args:
        beam: a Beam instance that has already had .solve() called.
        num_points: resolution of the plotted curves.

    Returns:
        The matplotlib Figure object (not shown automatically —
        call `.show()` or save it yourself, so this works headlessly
        in scripts/notebooks/servers alike).

    Raises:
        ImportError: if matplotlib is not installed.
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise ImportError(
            "matplotlib is required for plotting. "
            "Install with: uv sync --extra plots"
        ) from exc

    xs = [beam.length * i / num_points for i in range(num_points + 1)]
    shear = [beam.shear_at(x) for x in xs]
    moment = [beam.moment_at(x) for x in xs]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6), sharex=True)

    ax1.plot(xs, shear)
    ax1.axhline(0, color="black", linewidth=0.5)
    ax1.set_ylabel("Shear (N)")
    ax1.set_title("Shear Diagram")

    ax2.plot(xs, moment)
    ax2.axhline(0, color="black", linewidth=0.5)
    ax2.set_ylabel("Moment (N·m)")
    ax2.set_xlabel("Position along beam (m)")
    ax2.set_title("Bending Moment Diagram")

    fig.tight_layout()
    return fig
