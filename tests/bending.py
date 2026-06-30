"""
Roll Shaft -- Reaction, Shear & Moment Analysis
=================================================
Interactive Python version (numpy + matplotlib) of the beam statics tool.

Model
-----
    O ---- [friction zone x1..x2, F_f = mu*N] ---- A ---------- B
    ^pin reaction R_Oz                              ^pin reaction R_Az      ^known load F_g

  - O and A are pin supports -> two unknown vertical reactions R_Oz, R_Az.
  - F_g is a KNOWN applied load at B (not a reaction).
  - F_f = mu*N is modeled two ways at the same time:
      (a) concentrated point load at the centroid of the zone (x1+x2)/2
      (b) uniformly distributed load (UDL) spread across [x1, x2]
  - Because a UDL's centroid is its midpoint, R_Oz / R_Az come out IDENTICAL
    for both cases -- only the internal shear V(x) and moment M(x) *inside*
    the friction zone differ (step vs. ramp in shear, kink vs. smooth curve
    in moment).

Run
---
    pip install numpy matplotlib --break-system-packages
    python3 roll_shaft_beam_analysis.py

Use the sliders to drag x1, x2, x_A, x_B, mu, N, F_g and watch the
schematic + reactions + shear/moment diagrams update live. Click "Reset"
to return to the defaults shown in the original hand sketch.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from matplotlib.patches import FancyArrow

# ----------------------------------------------------------------------
# Defaults (edit these, or just drag the sliders once the window opens)
# ----------------------------------------------------------------------
DEFAULTS = dict(x1=1.0, x2=4.0, xA=6.0, xB=8.0, mu=0.30, N=200.0, Fg=80.0)

N_POINTS = 800  # resolution of the integrated V(x), M(x) curves


# ----------------------------------------------------------------------
# Statics
# ----------------------------------------------------------------------
def solve_reactions(x1, x2, xA, xB, mu, N, Fg):
    """Solve R_Oz, R_Az from sum(F)=0 and sum(M about O)=0."""
    Ff = mu * N
    xc = 0.5 * (x1 + x2)                      # centroid of the UDL == midpoint
    RA = (Ff * xc + Fg * xB) / xA             # sum(M_O) = 0
    RO = Ff + Fg - RA                          # sum(F_y) = 0
    return Ff, xc, RO, RA


def shear_moment(x1, x2, xA, xB, Ff, xc, RO, RA, case):
    """
    Build V(x) and M(x) on a fine grid for case 'a' (concentrated) or
    'b' (distributed UDL across [x1, x2]).
    """
    xs = np.linspace(0.0, xB, N_POINTS)
    dx = xs[1] - xs[0]
    q = Ff / (x2 - x1)  # UDL intensity for case b

    V = np.zeros_like(xs)
    v = 0.0
    applied_RO = applied_Ff = applied_RA = False

    for i, x in enumerate(xs):
        if not applied_RO and x >= 0:
            v += RO
            applied_RO = True

        if case == "a":
            if not applied_Ff and x >= xc:
                v -= Ff
                applied_Ff = True
        else:  # distributed
            if x1 < x <= x2:
                v -= q * dx

        if not applied_RA and x >= xA:
            v += RA
            applied_RA = True

        V[i] = v

    M = np.concatenate(([0.0], np.cumsum((V[:-1] + V[1:]) / 2.0 * dx)))
    return xs, V, M


# ----------------------------------------------------------------------
# Figure / layout
# ----------------------------------------------------------------------
plt.rcParams["font.family"] = "monospace"

fig = plt.figure(figsize=(11, 10))
fig.patch.set_facecolor("#0c1620")

gs = fig.add_gridspec(
    4, 1, height_ratios=[1.1, 1.4, 1.4, 2.6], hspace=0.55,
    left=0.09, right=0.97, top=0.96, bottom=0.04
)
ax_schem = fig.add_subplot(gs[0])
ax_shear = fig.add_subplot(gs[1])
ax_moment = fig.add_subplot(gs[2])
ax_ctrl = fig.add_subplot(gs[3])
ax_ctrl.axis("off")

PANEL_BG = "#101e2c"
GRID_C = "#1c3142"
INK = "#d9e6ec"
INK_DIM = "#7e98a8"
TEAL = "#3fd1c4"
AMBER = "#e8a23d"
RED = "#e0606a"

for ax in (ax_schem, ax_shear, ax_moment):
    ax.set_facecolor(PANEL_BG)
    ax.tick_params(colors=INK_DIM, labelsize=8)
    for spine in ax.spines.values():
        spine.set_color(GRID_C)
    ax.grid(True, color=GRID_C, linewidth=0.6)

ax_schem.set_title("Schematic", color=INK_DIM, fontsize=10, loc="left")
ax_shear.set_title("Shear diagram  V(x)", color=INK_DIM, fontsize=10, loc="left")
ax_moment.set_title("Moment diagram  M(x)", color=INK_DIM, fontsize=10, loc="left")

reactions_text = fig.text(
    0.09, 0.985, "", color=AMBER, fontsize=10, va="top", family="monospace"
)

# ----------------------------------------------------------------------
# Sliders (placed inside ax_ctrl's area, stacked)
# ----------------------------------------------------------------------
slider_specs = [
    ("x1", "x1  friction zone start", 0.2, 3.8, DEFAULTS["x1"]),
    ("x2", "x2  friction zone end", 1.0, 6.0, DEFAULTS["x2"]),
    ("xA", "x_A  support A position", 4.5, 9.0, DEFAULTS["xA"]),
    ("xB", "x_B  load point B", 5.0, 11.0, DEFAULTS["xB"]),
    ("mu", "mu  friction coefficient", 0.05, 0.8, DEFAULTS["mu"]),
    ("N", "N  normal force", 20, 500, DEFAULTS["N"]),
    ("Fg", "F_g  applied load at B", 0, 400, DEFAULTS["Fg"]),
]

sliders = {}
n_sliders = len(slider_specs)
slider_top, slider_bottom = 0.34, 0.02
slot_h = (slider_top - slider_bottom) / n_sliders

for i, (key, label, lo, hi, default) in enumerate(slider_specs):
    y = slider_top - (i + 1) * slot_h + slot_h * 0.25
    sax = fig.add_axes([0.30, y, 0.55, slot_h * 0.45])
    sax.set_facecolor(PANEL_BG)
    s = Slider(sax, label, lo, hi, valinit=default, color=TEAL,
               initcolor="none", track_color=GRID_C)
    s.label.set_color(INK_DIM)
    s.label.set_fontsize(8.5)
    s.valtext.set_color(INK)
    s.valtext.set_fontsize(8.5)
    sliders[key] = s

reset_ax = fig.add_axes([0.30, 0.005, 0.12, 0.025])
reset_btn = Button(reset_ax, "Reset", color=PANEL_BG, hovercolor="#1c3142")
reset_btn.label.set_color(RED)
reset_btn.label.set_fontsize(8.5)

fig.text(0.09, slider_top + 0.015, "Drag to change geometry / loads:",
          color=INK_DIM, fontsize=9)


# ----------------------------------------------------------------------
# Drawing helpers
# ----------------------------------------------------------------------
def draw_arrow(ax, x, y_from, y_to, color, lw=2, label=None, label_dy=0):
    ax.annotate(
        "", xy=(x, y_to), xytext=(x, y_from),
        arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, mutation_scale=14),
    )
    if label:
        ax.text(x, y_to + label_dy, label, color=color, fontsize=8,
                 ha="center", va="bottom" if label_dy >= 0 else "top")


def render(_=None):
    v = {k: sliders[k].val for k in ["x1", "x2", "xA", "xB", "mu", "N", "Fg"]}
    # keep sane ordering
    if v["x2"] <= v["x1"]:
        v["x2"] = v["x1"] + 0.2
    if v["xA"] <= v["x2"]:
        v["xA"] = v["x2"] + 0.3
    if v["xB"] <= v["xA"]:
        v["xB"] = v["xA"] + 0.3

    Ff, xc, RO, RA = solve_reactions(**v)

    reactions_text.set_text(
        f"F_f = mu*N = {Ff:7.1f} N    x_c = {xc:5.2f} m    "
        f"R_Oz = {RO:7.1f} N    R_Az = {RA:7.1f} N"
    )

    xa_a, Va, Ma = shear_moment(v["x1"], v["x2"], v["xA"], v["xB"], Ff, xc, RO, RA, "a")
    xa_b, Vb, Mb = shear_moment(v["x1"], v["x2"], v["xA"], v["xB"], Ff, xc, RO, RA, "b")

    # ---- schematic ----
    ax_schem.clear()
    ax_schem.set_facecolor(PANEL_BG)
    ax_schem.grid(True, color=GRID_C, linewidth=0.6)
    ax_schem.set_xlim(-0.5, v["xB"] * 1.15)
    ax_schem.set_ylim(-1.6, 1.6)
    ax_schem.set_yticks([])
    ax_schem.axhline(0, color=INK, lw=2)

    # reactions, upward
    draw_arrow(ax_schem, 0, -1.3, -0.02, AMBER, label=f"R_Oz={RO:.0f}", label_dy=-0.35)
    draw_arrow(ax_schem, v["xA"], -1.3, -0.02, AMBER, label=f"R_Az={RA:.0f}", label_dy=-0.35)

    # friction zone, downward arrows
    for xf in np.linspace(v["x1"], v["x2"], 9):
        draw_arrow(ax_schem, xf, 1.1, 0.05, RED, lw=1.4)
    ax_schem.text((v["x1"] + v["x2"]) / 2, 1.25, f"F_f = mu N = {Ff:.0f} N",
                  color=RED, fontsize=8, ha="center")

    # F_g at B, downward
    draw_arrow(ax_schem, v["xB"], 1.45, 0.05, TEAL, label=f"F_g={v['Fg']:.0f}", label_dy=0.05)

    for label, xpos in [("O", 0), ("A", v["xA"]), ("B", v["xB"])]:
        ax_schem.axvline(xpos, color="#3a5468", lw=0.8, ls=":")
        ax_schem.text(xpos, -1.55, label, color=INK_DIM, fontsize=9, ha="center")
    ax_schem.set_title("Schematic", color=INK_DIM, fontsize=10, loc="left")

    # ---- shear ----
    ax_shear.clear()
    ax_shear.set_facecolor(PANEL_BG)
    ax_shear.grid(True, color=GRID_C, linewidth=0.6)
    ax_shear.axhline(0, color="#3a5468", lw=1)
    ax_shear.plot(xa_a, Va, color=AMBER, lw=2, ls="--", label="(a) concentrated")
    ax_shear.plot(xa_b, Vb, color=TEAL, lw=2, label="(b) distributed (UDL)")
    for label, xpos in [("O", 0), ("A", v["xA"]), ("B", v["xB"])]:
        ax_shear.axvline(xpos, color="#3a5468", lw=0.8, ls=":")
    ax_shear.legend(facecolor=PANEL_BG, edgecolor=GRID_C, labelcolor=INK, fontsize=8, loc="best")
    ax_shear.set_ylabel("V  (N)", color=INK_DIM, fontsize=9)
    ax_shear.tick_params(colors=INK_DIM, labelsize=8)
    ax_shear.set_title("Shear diagram  V(x)", color=INK_DIM, fontsize=10, loc="left")

    # ---- moment ----
    ax_moment.clear()
    ax_moment.set_facecolor(PANEL_BG)
    ax_moment.grid(True, color=GRID_C, linewidth=0.6)
    ax_moment.axhline(0, color="#3a5468", lw=1)
    ax_moment.plot(xa_a, Ma, color=AMBER, lw=2, ls="--", label="(a) concentrated")
    ax_moment.plot(xa_b, Mb, color=TEAL, lw=2, label="(b) distributed (UDL)")
    for label, xpos in [("O", 0), ("A", v["xA"]), ("B", v["xB"])]:
        ax_moment.axvline(xpos, color="#3a5468", lw=0.8, ls=":")
    ax_moment.legend(facecolor=PANEL_BG, edgecolor=GRID_C, labelcolor=INK, fontsize=8, loc="best")
    ax_moment.set_xlabel("x  (m)", color=INK_DIM, fontsize=9)
    ax_moment.set_ylabel("M  (N·m)", color=INK_DIM, fontsize=9)
    ax_moment.tick_params(colors=INK_DIM, labelsize=8)
    ax_moment.set_title("Moment diagram  M(x)", color=INK_DIM, fontsize=10, loc="left")

    fig.canvas.draw_idle()


def reset(_):
    for key, val in DEFAULTS.items():
        sliders[key].set_val(val)
    render()


for s in sliders.values():
    s.on_changed(render)
reset_btn.on_clicked(reset)

render()
plt.show()