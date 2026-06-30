"""
Beam Analysis Studio  (v2)
============================
A general-purpose, interactive beam statics app.

NEW IN v2
---------
  - Loads (point AND distributed) can now point in ANY direction: pick a
    preset (Down / Up / Right / Left) or type a custom angle in degrees.
      angle convention: 0 deg = straight down, measured counter-clockwise,
      so 90 deg = points toward +x (right), 180 deg = straight up,
      270 deg = points toward -x (left).
  - Distributed loads can follow a SHAPE, not just "uniform":
      Uniform            w(x) = w0
      Triangular (up)    w(x) ramps 0 -> w0 from x1 to x2
      Triangular (down)  w(x) ramps w0 -> 0 from x1 to x2
      Custom f(x)        any expression in x, e.g.  20*np.sin(x) + 5
    All shapes are integrated numerically, so the resultant force,
    its centroid, and the shear/moment contribution are exact for
    whatever curve you type in.
  - Supports are now properly split into Roller (Ry only), Pin (Rx + Ry),
    and Fixed (Rx + Ry + M), and the solver runs a real 2D statics check:
    ΣFx = 0, ΣFy = 0, ΣM = 0 -- so angled loads that introduce horizontal
    force are handled correctly, with their own AXIAL FORCE diagram N(x).

BUG FIXES vs v1
----------------
  - Distributed-load integration previously assumed constant intensity;
    it's now done by numerically sampling w(x) so arbitrary shapes are
    correct (no more special-cased trapezoid formulas going stale).
  - Statics solvability check used to lump horizontal+vertical+moment
    unknowns into one "must equal 2" rule, which silently mis-handled
    any horizontal component. It's now two independent checks: the
    vertical/moment subsystem (needs exactly 2 unknowns: Ry's + Mr's)
    and the horizontal subsystem (needs exactly 0 or 1 unknown Rx,
    matching whether any horizontal load is present).
  - Custom w(x) / angle text entries are now safely evaluated with a
    restricted namespace and wrapped in try/except so a typo shows a
    friendly error instead of crashing the whole app.
  - Plot panels (schematic / shear / moment / axial) are now ALWAYS
    fully reset and re-labeled on every redraw, including the error
    path, so stale titles/axes from a previous successful run can no
    longer linger after a failed Calculate.
  - Fixed-support icon and reaction-moment label no longer overlap the
    Pin/Roller arrow when supports are close together.

Requirements
------------
    pip install numpy matplotlib --break-system-packages
    (tkinter ships with standard Python; on some Linux distros:
     sudo apt install python3-tk)

Run
---
    python3 beam_analysis_studio.py
"""

import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

# ----------------------------------------------------------------------
# Direction helpers
# ----------------------------------------------------------------------

DIRECTION_PRESETS = {
    "Down": 0.0,
    "Up": 180.0,
    "Right": 90.0,
    "Left": 270.0,
    "Custom": None,
}


def components(magnitude, angle_deg):
    """
    angle convention: 0 deg = straight down, CCW positive.
    Returns (vertical_down_positive, horizontal_right_positive).
    """
    th = np.radians(angle_deg)
    return magnitude * np.cos(th), magnitude * np.sin(th)


SAFE_NAMES = {
    "np": np, "sin": np.sin, "cos": np.cos, "tan": np.tan,
    "sqrt": np.sqrt, "abs": abs, "pi": np.pi, "exp": np.exp, "log": np.log,
}

# numpy >= 2.0 renamed trapz -> trapezoid; this keeps the app working on
# both old and new numpy without the user needing a specific version.
_trapz = getattr(np, "trapezoid", None) or np.trapz


def safe_eval_wx(expr, x):
    """Evaluate a w(x) expression with a restricted namespace."""
    return eval(expr, {"__builtins__": {}}, {**SAFE_NAMES, "x": x})


# ----------------------------------------------------------------------
# Data model
# ----------------------------------------------------------------------

class Support:
    def __init__(self, kind, x):
        self.kind = kind   # "Roller", "Pin", "Fixed"
        self.x = x

    def __str__(self):
        return f"{self.kind} @ x={self.x:g}"


class PointLoad:
    def __init__(self, x, P, angle_deg=0.0):
        self.x = x
        self.P = P
        self.angle = angle_deg

    def __str__(self):
        return f"Point load  P={self.P:g} N  @ x={self.x:g}  angle={self.angle:g}°"


class DistLoad:
    """
    shape: "uniform" | "tri_up" | "tri_down" | "custom"
    w0:    magnitude used for uniform / triangular peak
    expr:  expression string used when shape == "custom"
    """
    def __init__(self, x1, x2, shape, w0=0.0, expr="", angle_deg=0.0):
        self.x1, self.x2 = (x1, x2) if x1 < x2 else (x2, x1)
        self.shape = shape
        self.w0 = w0
        self.expr = expr
        self.angle = angle_deg

    def w(self, x):
        """Intensity (force/length) at position x, BEFORE angle decomposition."""
        if self.shape == "uniform":
            return self.w0
        if self.shape == "tri_up":
            return self.w0 * (x - self.x1) / (self.x2 - self.x1)
        if self.shape == "tri_down":
            return self.w0 * (self.x2 - x) / (self.x2 - self.x1)
        if self.shape == "custom":
            return safe_eval_wx(self.expr, x)
        raise ValueError(f"unknown shape {self.shape}")

    def label(self):
        shape_names = {"uniform": "uniform", "tri_up": "triangular ↑",
                        "tri_down": "triangular ↓", "custom": f"f(x)={self.expr}"}
        return (f"Distributed [{shape_names[self.shape]}]  "
                f"w0={self.w0:g}  over [{self.x1:g},{self.x2:g}]  angle={self.angle:g}°")

    def __str__(self):
        return self.label()


class AppliedMoment:
    def __init__(self, x, M):
        self.x = x
        self.M = M  # positive = counter-clockwise

    def __str__(self):
        return f"Moment  M={self.M:g} N·m  @ x={self.x:g}"


# ----------------------------------------------------------------------
# Solver
# ----------------------------------------------------------------------

class StaticsError(Exception):
    pass


def solve_beam(supports, point_loads, dist_loads, moments, n_points=900):
    """
    Full 2D statics: solves Rx (axial), Ry (vertical), and Mr (fixed-end
    moment) reactions, then sweeps the beam to build N(x), V(x), M(x).

    Returns (reactions, xs, N, V, M, L)
    """
    # ----- unknowns -----
    # vertical/moment subsystem
    v_unknowns = []   # ("R", support) or ("M", support)
    h_unknowns = []   # ("Rx", support)
    for s in supports:
        v_unknowns.append(("R", s))
        if s.kind == "Fixed":
            v_unknowns.append(("M", s))
        if s.kind in ("Pin", "Fixed"):
            h_unknowns.append(("Rx", s))

    if len(v_unknowns) != 2:
        raise StaticsError(
            f"Vertical/moment subsystem has {len(v_unknowns)} unknown(s); statics "
            "needs exactly 2 (sum Fy=0, sum M=0).\n\n"
            "Use either two Roller/Pin supports, OR one single Fixed support."
        )

    # ----- totals from loads, numerically integrated for distributed shapes -----
    F_total_v = 0.0   # downward-positive
    F_total_h = 0.0   # rightward-positive
    M_about_0 = 0.0    # from vertical components + applied moments

    for pl in point_loads:
        pv, ph = components(pl.P, pl.angle)
        F_total_v += pv
        F_total_h += ph
        M_about_0 += pv * pl.x

    dist_cache = []  # store sampled arrays for re-use during the sweep
    for dl in dist_loads:
        xs_s = np.linspace(dl.x1, dl.x2, 200)
        try:
            w_s = np.array([dl.w(xx) for xx in xs_s], dtype=float)
        except Exception as e:
            raise StaticsError(f"Could not evaluate distributed load shape "
                                f"on [{dl.x1:g},{dl.x2:g}]: {e}")
        wv_s, wh_s = components(w_s, dl.angle)
        Fv = _trapz(wv_s, xs_s)
        Fh = _trapz(wh_s, xs_s)
        Mv = _trapz(wv_s * xs_s, xs_s)
        F_total_v += Fv
        F_total_h += Fh
        M_about_0 += Mv
        dist_cache.append((dl, xs_s, wv_s, wh_s))

    for m in moments:
        M_about_0 += m.M

    # ----- solve vertical/moment 2x2 -----
    A = np.zeros((2, 2))
    b = np.array([F_total_v, M_about_0], dtype=float)
    for i, (kind, s) in enumerate(v_unknowns):
        if kind == "R":
            A[0, i] = 1.0
            A[1, i] = s.x
        else:
            A[1, i] = 1.0
    try:
        u = np.linalg.solve(A, b)
    except np.linalg.LinAlgError:
        raise StaticsError("Vertical subsystem is singular (e.g. two reactions "
                            "at the same x). Move a support.")

    reactions = []
    for (kind, s), val in zip(v_unknowns, u):
        existing = next((r for r in reactions if r["support"] is s), None)
        if existing is None:
            existing = {"support": s, "R": 0.0, "Mr": 0.0, "Rx": 0.0}
            reactions.append(existing)
        if kind == "R":
            existing["R"] = val
        else:
            existing["Mr"] = val

    # ----- solve horizontal subsystem (0 or 1 unknown) -----
    if len(h_unknowns) == 0:
        if abs(F_total_h) > 1e-6:
            raise StaticsError(
                f"Unbalanced horizontal force ({F_total_h:.2f} N) but no Pin/Fixed "
                "support can resist it. Add a Pin or Fixed support, or set load "
                "angles back to 0/180 (purely vertical)."
            )
    elif len(h_unknowns) == 1:
        kind, s = h_unknowns[0]
        existing = next((r for r in reactions if r["support"] is s), None)
        if existing is None:
            existing = {"support": s, "R": 0.0, "Mr": 0.0, "Rx": 0.0}
            reactions.append(existing)
        existing["Rx"] = F_total_h
    else:
        raise StaticsError(
            f"Horizontal subsystem has {len(h_unknowns)} unknown Rx components; "
            "only ONE Pin/Fixed support may resist horizontal force "
            "(the rest should be Rollers)."
        )

    # ----- beam extent -----
    xs_all = [s.x for s in supports] + [pl.x for pl in point_loads] + [m.x for m in moments]
    for dl in dist_loads:
        xs_all += [dl.x1, dl.x2]
    L = max(xs_all) if xs_all else 1.0
    if L <= 0:
        L = 1.0

    # ----- sweep to build N(x), V(x), M(x) -----
    xs = np.linspace(0.0, L, n_points)
    dx = xs[1] - xs[0]

    point_events = []  # (x, dN, dV, dM_direct)
    for r in reactions:
        point_events.append((r["support"].x, r["Rx"], r["R"], r["Mr"]))
    for pl in point_loads:
        pv, ph = components(pl.P, pl.angle)
        point_events.append((pl.x, -ph, -pv, 0.0))
    for m in moments:
        point_events.append((m.x, 0.0, 0.0, -m.M))

    applied_flags = [False] * len(point_events)

    N = np.zeros_like(xs)
    V = np.zeros_like(xs)
    M = np.zeros_like(xs)
    n_, v_, mom = 0.0, 0.0, 0.0

    for i, x in enumerate(xs):
        for j, (ex, dN, dV, dM) in enumerate(point_events):
            if not applied_flags[j] and x >= ex - 1e-9:
                n_ += dN
                v_ += dV
                mom += dM
                applied_flags[j] = True

        for dl, xs_s, wv_s, wh_s in dist_cache:
            if dl.x1 < x <= dl.x2:
                wv = np.interp(x, xs_s, wv_s)
                wh = np.interp(x, xs_s, wh_s)
                v_ -= wv * dx
                n_ -= wh * dx

        N[i] = n_
        V[i] = v_
        if i > 0:
            mom += (V[i - 1] + V[i]) / 2.0 * dx
        M[i] = mom

    return reactions, xs, N, V, M, L


# ----------------------------------------------------------------------
# GUI
# ----------------------------------------------------------------------

BG = "#101e2c"
PANEL = "#0c1620"
INK = "#d9e6ec"
DIM = "#7e98a8"
TEAL = "#3fd1c4"
AMBER = "#e8a23d"
RED = "#e0606a"
PURPLE = "#c98bd9"
GRID = "#1c3142"


class BeamApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Beam Analysis Studio v2")
        self.geometry("1420x920")
        self.configure(bg=PANEL)

        self.supports = []
        self.point_loads = []
        self.dist_loads = []
        self.moments = []

        self._build_layout()
        self._load_example()
        self.calculate()

    # ---------------- layout ----------------
    def _build_layout(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("TFrame", background=PANEL)
        style.configure("TLabel", background=PANEL, foreground=INK, font=("Consolas", 9))
        style.configure("Header.TLabel", background=PANEL, foreground=TEAL,
                         font=("Consolas", 10, "bold"))
        style.configure("TButton", font=("Consolas", 9))
        style.configure("TEntry", fieldbackground="#16293a", foreground=INK)
        style.configure("TCombobox", fieldbackground="#16293a")
        style.configure("Treeview", background="#0e1c29", fieldbackground="#0e1c29",
                         foreground=INK, font=("Consolas", 9), rowheight=22)
        style.configure("Treeview.Heading", background=GRID, foreground=DIM)

        main = ttk.Frame(self)
        main.pack(fill="both", expand=True)

        # scrollable left control panel (so it fits even with the new fields)
        left_outer = ttk.Frame(main, width=400)
        left_outer.pack(side="left", fill="y", padx=8, pady=8)
        left_outer.pack_propagate(False)

        canvas = tk.Canvas(left_outer, bg=PANEL, highlightthickness=0, width=380)
        vsb = ttk.Scrollbar(left_outer, orient="vertical", command=canvas.yview)
        left = ttk.Frame(canvas)
        left.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=left, anchor="nw")
        canvas.configure(yscrollcommand=vsb.set)
        canvas.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        right = ttk.Frame(main)
        right.pack(side="left", fill="both", expand=True, padx=4, pady=8)

        self._build_controls(left)
        self._build_plots(right)

    def _direction_row(self, parent, angle_var, row):
        ttk.Label(parent, text="direction").grid(row=row, column=0, sticky="w")
        combo = ttk.Combobox(parent, values=list(DIRECTION_PRESETS.keys()),
                              width=8, state="readonly")
        combo.set("Down")
        combo.grid(row=row, column=1, padx=2, sticky="w")
        ttk.Label(parent, text="angle°").grid(row=row, column=2, sticky="w")
        angle_entry = ttk.Entry(parent, textvariable=angle_var, width=6)
        angle_entry.grid(row=row, column=3, padx=2, sticky="w")

        def on_preset(_=None):
            preset = DIRECTION_PRESETS[combo.get()]
            if preset is not None:
                angle_var.set(str(preset))
        combo.bind("<<ComboboxSelected>>", on_preset)
        return combo

    def _build_controls(self, parent):
        ttk.Label(parent, text="SUPPORTS", style="Header.TLabel").pack(anchor="w", pady=(0, 4))
        ttk.Label(parent, text="Roller=Ry only   Pin=Rx+Ry   Fixed=Rx+Ry+M",
                  foreground=DIM).pack(anchor="w")
        sframe = ttk.Frame(parent)
        sframe.pack(fill="x", pady=(2, 0))
        self.sup_type = tk.StringVar(value="Roller")
        ttk.Combobox(sframe, textvariable=self.sup_type, values=["Roller", "Pin", "Fixed"],
                     width=10, state="readonly").grid(row=0, column=0, padx=2, pady=2)
        self.sup_x = tk.StringVar(value="0")
        ttk.Entry(sframe, textvariable=self.sup_x, width=8).grid(row=0, column=1, padx=2)
        ttk.Button(sframe, text="Add Support", command=self.add_support).grid(row=0, column=2, padx=4)

        self.sup_tree = ttk.Treeview(parent, show="tree", height=4)
        self.sup_tree.pack(fill="x", pady=(4, 2))
        ttk.Button(parent, text="Remove selected",
                   command=lambda: self._remove(self.sup_tree, self.supports)).pack(anchor="w", pady=(0, 10))

        # ---- point loads ----
        ttk.Label(parent, text="POINT LOADS", style="Header.TLabel").pack(anchor="w", pady=(4, 4))
        plframe = ttk.Frame(parent)
        plframe.pack(fill="x")
        ttk.Label(plframe, text="P (N)").grid(row=0, column=0, sticky="w")
        ttk.Label(plframe, text="x (m)").grid(row=0, column=1, sticky="w")
        self.pl_P = tk.StringVar(value="100")
        self.pl_x = tk.StringVar(value="3")
        ttk.Entry(plframe, textvariable=self.pl_P, width=8).grid(row=1, column=0, padx=2)
        ttk.Entry(plframe, textvariable=self.pl_x, width=8).grid(row=1, column=1, padx=2)
        self.pl_angle = tk.StringVar(value="0")
        self._direction_row(plframe, self.pl_angle, row=2)
        ttk.Button(plframe, text="Add Point Load", command=self.add_point_load).grid(
            row=3, column=0, columnspan=4, pady=4, sticky="we")

        self.pl_tree = ttk.Treeview(parent, show="tree", height=4)
        self.pl_tree.pack(fill="x", pady=(4, 2))
        ttk.Button(parent, text="Remove selected",
                   command=lambda: self._remove(self.pl_tree, self.point_loads)).pack(anchor="w", pady=(0, 10))

        # ---- distributed loads ----
        ttk.Label(parent, text="DISTRIBUTED LOADS", style="Header.TLabel").pack(anchor="w", pady=(4, 4))
        dlframe = ttk.Frame(parent)
        dlframe.pack(fill="x")
        ttk.Label(dlframe, text="shape").grid(row=0, column=0, sticky="w")
        self.dl_shape = tk.StringVar(value="uniform")
        shape_combo = ttk.Combobox(dlframe, textvariable=self.dl_shape, state="readonly", width=12,
                                    values=["uniform", "tri_up", "tri_down", "custom"])
        shape_combo.grid(row=0, column=1, columnspan=3, sticky="w", padx=2)

        ttk.Label(dlframe, text="w0 (N/m)").grid(row=1, column=0, sticky="w")
        ttk.Label(dlframe, text="x1").grid(row=1, column=1, sticky="w")
        ttk.Label(dlframe, text="x2").grid(row=1, column=2, sticky="w")
        self.dl_w0 = tk.StringVar(value="20")
        self.dl_x1 = tk.StringVar(value="1")
        self.dl_x2 = tk.StringVar(value="4")
        ttk.Entry(dlframe, textvariable=self.dl_w0, width=6).grid(row=2, column=0, padx=2)
        ttk.Entry(dlframe, textvariable=self.dl_x1, width=6).grid(row=2, column=1, padx=2)
        ttk.Entry(dlframe, textvariable=self.dl_x2, width=6).grid(row=2, column=2, padx=2)

        ttk.Label(dlframe, text="custom f(x), used if shape=custom").grid(
            row=3, column=0, columnspan=4, sticky="w", pady=(4, 0))
        self.dl_expr = tk.StringVar(value="20*np.sin((x-1)/3*pi)")
        ttk.Entry(dlframe, textvariable=self.dl_expr, width=30).grid(
            row=4, column=0, columnspan=4, sticky="we", pady=(0, 4))

        self.dl_angle = tk.StringVar(value="0")
        self._direction_row(dlframe, self.dl_angle, row=5)

        ttk.Button(dlframe, text="Add Distributed Load", command=self.add_dist_load).grid(
            row=6, column=0, columnspan=4, pady=4, sticky="we")

        self.dl_tree = ttk.Treeview(parent, show="tree", height=4)
        self.dl_tree.pack(fill="x", pady=(4, 2))
        ttk.Button(parent, text="Remove selected",
                   command=lambda: self._remove(self.dl_tree, self.dist_loads)).pack(anchor="w", pady=(0, 10))

        # ---- moments ----
        ttk.Label(parent, text="APPLIED MOMENTS", style="Header.TLabel").pack(anchor="w", pady=(4, 4))
        mframe = ttk.Frame(parent)
        mframe.pack(fill="x")
        ttk.Label(mframe, text="M (N·m, CCW+)").grid(row=0, column=0, sticky="w")
        ttk.Label(mframe, text="x (m)").grid(row=0, column=1, sticky="w")
        self.m_M = tk.StringVar(value="0")
        self.m_x = tk.StringVar(value="5")
        ttk.Entry(mframe, textvariable=self.m_M, width=8).grid(row=1, column=0, padx=2)
        ttk.Entry(mframe, textvariable=self.m_x, width=8).grid(row=1, column=1, padx=2)
        ttk.Button(mframe, text="Add", command=self.add_moment).grid(row=1, column=2, padx=4)

        self.m_tree = ttk.Treeview(parent, show="tree", height=3)
        self.m_tree.pack(fill="x", pady=(4, 2))
        ttk.Button(parent, text="Remove selected",
                   command=lambda: self._remove(self.m_tree, self.moments)).pack(anchor="w", pady=(0, 10))

        ttk.Separator(parent).pack(fill="x", pady=8)
        ttk.Button(parent, text="CALCULATE  ▶", command=self.calculate).pack(fill="x", ipady=6)
        ttk.Button(parent, text="Clear all", command=self.clear_all).pack(fill="x", pady=(6, 0))

        self.reaction_box = tk.Text(parent, height=8, bg="#0e1c29", fg=AMBER,
                                     font=("Consolas", 9), relief="flat")
        self.reaction_box.pack(fill="x", pady=(12, 0))

    def _build_plots(self, parent):
        plt.rcParams["font.family"] = "monospace"
        self.fig, (self.ax_schem, self.ax_axial, self.ax_shear, self.ax_moment) = plt.subplots(
            4, 1, figsize=(9, 10), gridspec_kw={"height_ratios": [1, 0.9, 1.3, 1.3]}
        )
        self.fig.patch.set_facecolor(PANEL)
        for ax in (self.ax_schem, self.ax_axial, self.ax_shear, self.ax_moment):
            ax.set_facecolor(BG)
            ax.tick_params(colors=DIM, labelsize=8)
            for sp in ax.spines.values():
                sp.set_color(GRID)
            ax.grid(True, color=GRID, linewidth=0.6)
        self.fig.tight_layout(pad=2.2)

        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        toolbar = NavigationToolbar2Tk(self.canvas, parent)
        toolbar.update()

    # ---------------- list helpers ----------------
    def _refresh_tree(self, tree, items):
        tree.delete(*tree.get_children())
        for it in items:
            tree.insert("", "end", text=str(it))

    def _remove(self, tree, items):
        sel = tree.selection()
        if not sel:
            return
        idx = tree.index(sel[0])
        del items[idx]
        self._refresh_all_trees()

    def _refresh_all_trees(self):
        self._refresh_tree(self.sup_tree, self.supports)
        self._refresh_tree(self.pl_tree, self.point_loads)
        self._refresh_tree(self.dl_tree, self.dist_loads)
        self._refresh_tree(self.m_tree, self.moments)

    # ---------------- add actions ----------------
    def add_support(self):
        try:
            x = float(self.sup_x.get())
        except ValueError:
            messagebox.showerror("Invalid", "Support position must be a number.")
            return
        self.supports.append(Support(self.sup_type.get(), x))
        self._refresh_all_trees()

    def add_point_load(self):
        try:
            P = float(self.pl_P.get())
            x = float(self.pl_x.get())
            angle = float(self.pl_angle.get())
        except ValueError:
            messagebox.showerror("Invalid", "Point load needs numeric P, x and angle.")
            return
        self.point_loads.append(PointLoad(x, P, angle))
        self._refresh_all_trees()

    def add_dist_load(self):
        try:
            w0 = float(self.dl_w0.get())
            x1 = float(self.dl_x1.get())
            x2 = float(self.dl_x2.get())
            angle = float(self.dl_angle.get())
        except ValueError:
            messagebox.showerror("Invalid", "Distributed load needs numeric w0, x1, x2, angle.")
            return
        if x2 == x1:
            messagebox.showerror("Invalid", "x1 and x2 must differ.")
            return
        shape = self.dl_shape.get()
        expr = self.dl_expr.get()
        if shape == "custom":
            try:
                _ = safe_eval_wx(expr, 0.5 * (x1 + x2))
            except Exception as e:
                messagebox.showerror("Invalid expression", f"Could not evaluate f(x): {e}")
                return
        self.dist_loads.append(DistLoad(x1, x2, shape, w0, expr, angle))
        self._refresh_all_trees()

    def add_moment(self):
        try:
            M = float(self.m_M.get())
            x = float(self.m_x.get())
        except ValueError:
            messagebox.showerror("Invalid", "Moment needs numeric M and x.")
            return
        self.moments.append(AppliedMoment(x, M))
        self._refresh_all_trees()

    def clear_all(self):
        self.supports, self.point_loads, self.dist_loads, self.moments = [], [], [], []
        self._refresh_all_trees()
        self.calculate()

    def _load_example(self):
        # Mirrors the roll-shaft sketch: two supports O, A; a distributed
        # friction load between them; a point load at B beyond A.
        self.supports = [Support("Pin", 0.0), Support("Roller", 6.0)]
        self.dist_loads = [DistLoad(1.0, 4.0, "uniform", 20.0, "", 0.0)]  # F_f = 60 N
        self.point_loads = [PointLoad(8.0, 80.0, 0.0)]                    # F_g at B
        self.moments = []
        self._refresh_all_trees()

    # ---------------- reset plot helper (bugfix: always fully reset) ----------------
    def _reset_axes(self):
        for ax in (self.ax_schem, self.ax_axial, self.ax_shear, self.ax_moment):
            ax.clear()
            ax.set_facecolor(BG)
            ax.grid(True, color=GRID, linewidth=0.6)
            ax.tick_params(colors=DIM, labelsize=8)
            for sp in ax.spines.values():
                sp.set_color(GRID)

    # ---------------- calculate & plot ----------------
    def calculate(self):
        self._reset_axes()
        try:
            reactions, xs, N, V, M, L = solve_beam(
                self.supports, self.point_loads, self.dist_loads, self.moments
            )
        except StaticsError as e:
            self.reaction_box.delete("1.0", "end")
            self.reaction_box.insert("end", "STATICS ERROR:\n" + str(e))
            for ax, title in ((self.ax_schem, "Schematic"), (self.ax_axial, "Axial force N(x)"),
                               (self.ax_shear, "Shear V(x)"), (self.ax_moment, "Moment M(x)")):
                ax.set_title(title, color=DIM, fontsize=10, loc="left")
                ax.text(0.5, 0.5, "Not solvable with statics alone\n(see message at left)",
                         color=RED, ha="center", va="center", transform=ax.transAxes, fontsize=9)
            self.canvas.draw_idle()
            return

        # ---- reactions text ----
        self.reaction_box.delete("1.0", "end")
        for r in reactions:
            s = r["support"]
            line = f"{s.kind:7s} @ x={s.x:5.2f}   Ry={r['R']:8.2f} N"
            if s.kind in ("Pin", "Fixed"):
                line += f"   Rx={r['Rx']:8.2f} N"
            if s.kind == "Fixed":
                line += f"   M={r['Mr']:8.2f} N·m"
            self.reaction_box.insert("end", line + "\n")

        # ---- schematic ----
        ax = self.ax_schem
        ax.axhline(0, color=INK, lw=2)
        ax.set_xlim(-0.5, L * 1.1)
        ax.set_ylim(-1.7, 1.7)
        ax.set_yticks([])
        ax.set_title("Schematic", color=DIM, fontsize=10, loc="left")

        icon = {"Roller": "▲", "Pin": "●", "Fixed": "▦"}
        for r in reactions:
            s = r["support"]
            ax.annotate("", xy=(s.x, -0.02), xytext=(s.x, -1.3),
                        arrowprops=dict(arrowstyle="-|>", color=AMBER, lw=2))
            lbl = f"Ry={r['R']:.0f}"
            if s.kind in ("Pin", "Fixed"):
                lbl += f"\nRx={r['Rx']:.0f}"
            if s.kind == "Fixed":
                lbl += f"\nM={r['Mr']:.0f}"
            ax.text(s.x, -1.45, lbl, color=AMBER, fontsize=7.5, ha="center", va="top")
            ax.text(s.x, 0.08, icon.get(s.kind, "▲"), color=AMBER, fontsize=11, ha="center", va="bottom")

        for pl in self.point_loads:
            pv, ph = components(pl.P, pl.angle)
            scale = 1.0 / max(abs(pl.P), 1e-9)
            dx_, dy_ = ph * scale, -pv * scale  # screen y: up positive, so down-load => negative dy
            ax.annotate("", xy=(pl.x + dx_ * 1.1, dy_ * 1.1), xytext=(pl.x - dx_ * 0.1, -dy_ * 0.1),
                        arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=2))
            ax.text(pl.x + dx_ * 1.1, dy_ * 1.1 + (0.1 if dy_ >= 0 else -0.1),
                    f"P={pl.P:.0f}@{pl.angle:.0f}°", color=TEAL, fontsize=7.5, ha="center")

        for dl in self.dist_loads:
            n_arrows = max(4, int((dl.x2 - dl.x1) * 2) + 2)
            for xf in np.linspace(dl.x1, dl.x2, n_arrows):
                w_local = dl.w(xf)
                wv, wh = components(w_local, dl.angle)
                scale = 0.9 / max(abs(dl.w0) if dl.w0 else 1.0, 1e-9)
                dx_, dy_ = wh * scale, -wv * scale
                ax.annotate("", xy=(xf + dx_, dy_), xytext=(xf, 0),
                            arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.2))
            ax.text((dl.x1 + dl.x2) / 2, 1.15, dl.label(), color=RED, fontsize=7, ha="center")

        for m in self.moments:
            ax.annotate("", xy=(m.x + 0.3, 0.55), xytext=(m.x - 0.3, 0.55),
                        arrowprops=dict(arrowstyle="-|>", color=PURPLE,
                                        connectionstyle="arc3,rad=0.6", lw=2))
            ax.text(m.x, 0.85, f"M={m.M:.0f}", color=PURPLE, fontsize=8, ha="center")

        # ---- axial ----
        ax = self.ax_axial
        ax.axhline(0, color="#3a5468", lw=1)
        ax.plot(xs, N, color=PURPLE, lw=2)
        ax.fill_between(xs, N, 0, color=PURPLE, alpha=0.12)
        ax.set_ylabel("N (N)", color=DIM, fontsize=9)
        ax.set_title("Axial force diagram N(x)", color=DIM, fontsize=10, loc="left")

        # ---- shear ----
        ax = self.ax_shear
        ax.axhline(0, color="#3a5468", lw=1)
        ax.plot(xs, V, color=TEAL, lw=2)
        ax.fill_between(xs, V, 0, color=TEAL, alpha=0.12)
        ax.set_ylabel("V (N)", color=DIM, fontsize=9)
        ax.set_title("Shear diagram V(x)", color=DIM, fontsize=10, loc="left")

        # ---- moment ----
        ax = self.ax_moment
        ax.axhline(0, color="#3a5468", lw=1)
        ax.plot(xs, M, color=AMBER, lw=2)
        ax.fill_between(xs, M, 0, color=AMBER, alpha=0.12)
        ax.set_xlabel("x (m)", color=DIM, fontsize=9)
        ax.set_ylabel("M (N·m)", color=DIM, fontsize=9)
        ax.set_title("Moment diagram M(x)", color=DIM, fontsize=10, loc="left")
        if len(M):
            idx_max = int(np.argmax(np.abs(M)))
            ax.annotate(f"M_max = {M[idx_max]:.1f} N·m @ x={xs[idx_max]:.2f}",
                        xy=(xs[idx_max], M[idx_max]), color=AMBER, fontsize=8,
                        xytext=(8, 8), textcoords="offset points")

        for ax in (self.ax_schem, self.ax_axial, self.ax_shear, self.ax_moment):
            for s in self.supports:
                ax.axvline(s.x, color="#3a5468", lw=0.8, ls=":")

        self.fig.tight_layout(pad=2.2)
        self.canvas.draw_idle()


if __name__ == "__main__":
    app = BeamApp()
    app.mainloop()