"""
interfaces.visual.plots — shear/moment diagram plotting.

Requires matplotlib, which is an optional dependency (install with
`pip install mechlab[plots]` or `uv sync --extra plots`) so that core
mechlab usage never forces a plotting dependency on users who only
need numeric results (e.g. running in a headless service).
"""

from __future__ import annotations

from pathlib import Path


def plot_shear(
    beam,
    num_points: int = 200,
    save_path: str | Path | None = None,
    show: bool = False,
):
    """Plot the shear force diagram for a solved beam.

    Args:
        beam: a Beam instance that has already had .solve() called.
        num_points: resolution of the plotted curve.
        save_path: optional path to export the figure as an image.
        show: if True, block until the figure window is closed.

    Returns:
        The matplotlib Figure object.
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

    fig, ax = plt.subplots(figsize=(8, 4))

    ax.plot(xs, shear, color="blue")
    ax.axhline(0, color="black", linewidth=0.5)
    ax.set_ylabel("Shear (N)")
    ax.set_xlabel("Position along beam (m)")
    ax.set_title("Shear Diagram")
    ax.grid(True, linestyle="--", alpha=0.6)

    fig.tight_layout()

    if save_path is not None:
        fig.savefig(save_path, dpi=300, bbox_inches="tight")

    if show:
        plt.show()

    return fig


def plot_shear_moment(
    beam,
    num_points: int = 200,
    save_path: str | Path | None = None,
    show: bool = False,
):
    """Backward-compatible alias for plot_shear."""
    return plot_shear(
        beam,
        num_points=num_points,
        save_path=save_path,
        show=show,
    )


def plot_moment(
    beam,
    num_points: int = 200,
    save_path: str | Path | None = None,
    show: bool = False,
):
    """Plot the bending moment diagram for a solved beam.

    Args:
        beam: a Beam instance that has already had .solve() called.
        num_points: resolution of the plotted curve.
        save_path: optional path to export the figure as an image.
        show: if True, block until the figure window is closed.

    Returns:
        The matplotlib Figure object.
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise ImportError(
            "matplotlib is required for plotting. "
            "Install with: uv sync --extra plots"
        ) from exc

    xs = [beam.length * i / num_points for i in range(num_points + 1)]
    moment = [beam.moment_at(x) for x in xs]

    fig, ax = plt.subplots(figsize=(8, 4))

    ax.plot(xs, moment, color="red")
    ax.axhline(0, color="black", linewidth=0.5)
    ax.set_ylabel("Moment (N·m)")
    ax.set_xlabel("Position along beam (m)")
    ax.set_title("Bending Moment Diagram")
    ax.grid(True, linestyle="--", alpha=0.6)

    fig.tight_layout()

    if save_path is not None:
        fig.savefig(save_path, dpi=300, bbox_inches="tight")

    if show:
        plt.show()

    return fig



def plot_fbd_beam(beam, save_path: str | None = None, show: bool = False):
    """Plot the free body diagram of a solved beam, textbook style.

    Args:
        beam: a Beam instance that has already had .solve() called.
        save_path: optional path to export the figure as an image.
        show: if True, block until the figure window is closed.

    Returns:
        The matplotlib Figure object.
    """
    try:
        import matplotlib.patches as patches
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError as exc:
        raise ImportError(
            "matplotlib and numpy are required for plotting. "
            "Install with: pip install matplotlib numpy"
        ) from exc

    BEAM_Y = 0.0
    COLOR = "black"

    fig, ax = plt.subplots(figsize=(10, 5))

    # ------------------------------------------------------------------
    # 1. Classify loads and supports (duck typed, see module docstring)
    # ------------------------------------------------------------------
    point_loads, moment_loads, dist_loads = [], [], []
    for load in beam.loads:
        name = type(load).__name__
        if "Moment" in name:
            moment_loads.append(load)
        elif "Distributed" in name:
            dist_loads.append(load)
        else:
            point_loads.append(load)

    hinge_supports = [
        s for s in beam.supports if "HINGE" in str(getattr(s, "kind", "")).upper()
    ]
    reaction_supports = [s for s in beam.supports if s not in hinge_supports]

    # ------------------------------------------------------------------
    # 2. Scale for arrow lengths so nothing is too big or invisible
    # ------------------------------------------------------------------
    # plots.py, in force_mags
    force_mags = (
        [abs(load.magnitude) / 1000 for load in point_loads]
        + [abs(load.intensity) / 1000 for load in dist_loads]
        + [abs(getattr(s, "reaction_force", 0)) / 1000 for s in reaction_supports]
    )
    max_force = max(force_mags) if force_mags else 1.0
    ARROW_H = 1.3  # plot-coordinate height for the largest arrow

    def arrow_len(mag_kn: float) -> float:
        if max_force == 0:
            return 0.5
        return max(0.35, (abs(mag_kn) / max_force) * ARROW_H)

    def draw_force_arrow(x, tip_y, tail_y, color, label, ha="center", va="bottom"):
        ax.annotate(
            "",
            xy=(x, tip_y),
            xytext=(x, tail_y),
            arrowprops=dict(arrowstyle="-|>", color=color, lw=1.6, mutation_scale=14),
            zorder=4,
        )
        label_y = tail_y + (0.12 if tail_y > tip_y else -0.12)
        ax.text(
            x, label_y, label, ha=ha, va=va if tail_y > tip_y else "top",
            color=color, fontsize=10, fontweight="bold", zorder=5,
        )

    def draw_moment_arrow(x, y, magnitude, color="black", radius=0.28):
        """Small curved arrow representing an applied/reaction moment."""
        theta = np.linspace(20, 340, 40)
        sign = 1 if magnitude >= 0 else -1
        xs = x + radius * np.cos(np.radians(theta))
        ys = y + 0.55 + sign * radius * 0.9 * np.sin(np.radians(theta))
        ax.plot(xs, ys, color=color, lw=1.4, zorder=4)
        # arrowhead at the end of the curve
        ax.annotate(
            "",
            xy=(xs[-1], ys[-1]),
            xytext=(xs[-3], ys[-3]),
            arrowprops=dict(arrowstyle="-|>", color=color, lw=1.4, mutation_scale=10),
            zorder=4,
        )
        ax.text(
            x, y + 0.55 + radius * 1.6, f"{abs(magnitude) / 1000:.1f} kN\u00b7m",
            ha="center", va="bottom", color=color, fontsize=10, fontweight="bold",
        )

    def draw_hinge(x, y=BEAM_Y):
        ax.plot(x, y, "o", color=COLOR, markersize=5, zorder=5, markerfacecolor="white")
        arc = patches.Arc(
            (x, y), 0.5, 0.5, angle=0, theta1=200, theta2=340,
            color=COLOR, lw=1.2, zorder=4,
        )
        ax.add_patch(arc)

    # ------------------------------------------------------------------
    # 3. Beam line
    # ------------------------------------------------------------------
    ax.plot([0, beam.length], [BEAM_Y, BEAM_Y], color=COLOR, linewidth=4, zorder=2)

    # small "x ->" axis indicator, top-left
    ax.annotate(
        "", xy=(beam.length * 0.09, ARROW_H + 0.55),
        xytext=(0, ARROW_H + 0.55),
        arrowprops=dict(arrowstyle="-|>", color=COLOR, lw=1.2, mutation_scale=10),
    )
    ax.text(beam.length * 0.045, ARROW_H + 0.68, "x", ha="center", fontsize=10)

    # ------------------------------------------------------------------
    # 4. Reactions at supports
    # ------------------------------------------------------------------
    for support in reaction_supports:
        reaction_kn = getattr(support, "reaction_force", 0) / 1000
        if abs(reaction_kn) > 1e-3:
            is_up = reaction_kn > 0
            length = arrow_len(reaction_kn)
            tail_y = -length if is_up else length
            draw_force_arrow(
                support.position, BEAM_Y, tail_y, "tab:blue",
                f"{abs(reaction_kn):.1f} kN",
            )

        reaction_m = getattr(support, "reaction_moment", 0)
        if abs(reaction_m) > 1e-3:
            draw_moment_arrow(support.position, BEAM_Y, reaction_m, color="tab:blue")

    # ------------------------------------------------------------------
    # 5. Internal hinges (+ any moment load applied right at that point)
    # ------------------------------------------------------------------
    for hinge in hinge_supports:
        draw_hinge(hinge.position)

    for m in moment_loads:
        draw_moment_arrow(m.position, BEAM_Y, m.magnitude, color="tab:red")

    # ------------------------------------------------------------------
    # 6. Point loads
    # ------------------------------------------------------------------
    for load in point_loads:
        mag_kn = load.magnitude / 1000
        is_down = mag_kn > 0
        length = arrow_len(mag_kn)
        tail_y = length if is_down else -length
        draw_force_arrow(
            load.position, BEAM_Y, tail_y, "tab:red", f"{abs(mag_kn):.1f} kN",
        )

    # ------------------------------------------------------------------
    # 7. Distributed loads: bracket + evenly spaced arrows, no shading
    # ------------------------------------------------------------------
    for load in dist_loads:
        mag = load.intensity / 1000
        is_down = mag > 0
        length = arrow_len(mag)
        y_line = length if is_down else -length

        ax.plot([load.start, load.end], [y_line, y_line], color="tab:orange", lw=1)
        ax.plot([load.start, load.start], [y_line, y_line * 0.85], color="tab:orange", lw=1)
        ax.plot([load.end, load.end], [y_line, y_line * 0.85], color="tab:orange", lw=1)

        n_arrows = max(3, int(abs(load.end - load.start) * 1.5))
        for x in np.linspace(load.start, load.end, n_arrows):
            ax.annotate(
                "", xy=(x, 0.05 if is_down else -0.05), xytext=(x, y_line),
                arrowprops=dict(arrowstyle="-|>", color="tab:orange", lw=1.2, mutation_scale=9),
                zorder=3,
            )

        mid_x = (load.start + load.end) / 2
        ax.text(
            mid_x, y_line + (0.15 if is_down else -0.15), f"{abs(mag):.1f} kN/m",
            ha="center", va="bottom" if is_down else "top",
            color="tab:orange", fontsize=10, fontweight="bold",
        )

    # ------------------------------------------------------------------
    # 8. Auto-label key points along the beam: A, B, C, ...
    # ------------------------------------------------------------------
    key_positions = {0.0, float(beam.length)}
    key_positions.update(s.position for s in beam.supports)
    key_positions = sorted(key_positions)

    for letter, x in zip(_letters(), key_positions):
        ax.text(x, 0.18, letter, ha="center", va="bottom", fontsize=12, fontweight="bold")

    # ------------------------------------------------------------------
    # 9. Axis formatting
    # ------------------------------------------------------------------
    ax.get_yaxis().set_visible(False)
    for spine in ("left", "right", "top", "bottom"):
        ax.spines[spine].set_visible(False)

    ax.set_xlim(-beam.length * 0.06, beam.length * 1.06)
    ax.set_ylim(-ARROW_H - 1.0, ARROW_H + 1.0)
    ax.set_title("Free body diagram", fontsize=13, fontweight="bold", pad=18)

    fig.tight_layout()

    if save_path is not None:
        fig.savefig(save_path, dpi=300, bbox_inches="tight")
    if show:
        plt.show()

    return fig


def _letters():
    """Yield 'A', 'B', 'C', ... 'Z', 'AA', 'AB', ... forever."""
    import itertools
    import string

    for n in itertools.count(1):
        for combo in itertools.product(string.ascii_uppercase, repeat=n):
            yield "".join(combo)
