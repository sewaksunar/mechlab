"""
Beam Analysis Studio (v3) - Bright Theme & Proper FBD (with Data Querying)
==============================================================================
A general-purpose, scriptable beam statics library with isolated,
bright-themed plots, accurate vector anchoring, and precise data querying.
"""

import numpy as np
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------
# Direction & Math Helpers
# ----------------------------------------------------------------------

def components(magnitude, angle_deg):
    """Returns (vertical_down_positive, horizontal_right_positive)."""
    th = np.radians(angle_deg)
    return magnitude * np.cos(th), magnitude * np.sin(th)

SAFE_NAMES = {
    "np": np, "sin": np.sin, "cos": np.cos, "tan": np.tan,
    "sqrt": np.sqrt, "abs": abs, "pi": np.pi, "exp": np.exp, "log": np.log,
}

_trapz = getattr(np, "trapezoid", None) or np.trapz

def safe_eval_wx(expr, x):
    """Evaluate a w(x) expression safely with a restricted namespace."""
    return eval(expr, {"__builtins__": {}}, {**SAFE_NAMES, "x": x})


# ----------------------------------------------------------------------
# Data Model
# ----------------------------------------------------------------------

class Support:
    def __init__(self, kind, x):
        if kind not in ("Roller", "Pin", "Fixed"):
            raise ValueError("Support kind must be 'Roller', 'Pin', or 'Fixed'")
        self.kind = kind   
        self.x = x


class PointLoad:
    def __init__(self, x, P, angle_deg=0.0):
        self.x = x
        self.P = P
        self.angle = angle_deg


class DistLoad:
    def __init__(self, x1, x2, shape, w0=0.0, expr="", angle_deg=0.0):
        self.x1, self.x2 = (x1, x2) if x1 < x2 else (x2, x1)
        if shape not in ("uniform", "tri_up", "tri_down", "custom"):
            raise ValueError("Shape must be 'uniform', 'tri_up', 'tri_down', or 'custom'")
        self.shape = shape
        self.w0 = w0
        self.expr = expr
        self.angle = angle_deg

    def w(self, x):
        if self.shape == "uniform": return self.w0
        if self.shape == "tri_up": return self.w0 * (x - self.x1) / (self.x2 - self.x1)
        if self.shape == "tri_down": return self.w0 * (self.x2 - x) / (self.x2 - self.x1)
        if self.shape == "custom": return safe_eval_wx(self.expr, x)
        raise ValueError(f"Unknown shape {self.shape}")

    def label(self):
        shape_names = {"uniform": "uniform", "tri_up": r"triangular $\uparrow$",
                       "tri_down": r"triangular $\downarrow$", "custom": fr"$f(x)={self.expr}$"}
        return fr"Distributed [{shape_names[self.shape]}] $w_0={self.w0:g}$ over $x \in [{self.x1:g}, {self.x2:g}]$"


class AppliedMoment:
    def __init__(self, x, M):
        self.x = x
        self.M = M  


# ----------------------------------------------------------------------
# Core Beam Studio Class
# ----------------------------------------------------------------------

class StaticsError(Exception):
    pass


class BeamStudio:
    def __init__(self):
        self.supports = []
        self.point_loads = []
        self.dist_loads = []
        self.moments = []
        self._cached_solution = None # Caches (reactions, xs, N, V, M_diag, L)
        
        # --------------------------------------------------
        # Bright Theme Palette
        # --------------------------------------------------
        self.bg_color = "#ffffff"       
        self.panel_color = "#f8f9fa"    
        self.ink_color = "#212529"      
        self.dim_color = "#495057"      
        self.teal_color = "#0284c7"     
        self.amber_color = "#d97706"    
        self.red_color = "#dc2626"      
        self.purple_color = "#7c3aed"   
        self.grid_color = "#e5e7eb"     
        
        plt.rcParams["font.family"] = "monospace"
        plt.rcParams["mathtext.fontset"] = "cm" 

    def add_support(self, kind, x): 
        self.supports.append(Support(kind, float(x)))
        self._cached_solution = None

    def add_point_load(self, x, P, angle_deg=0.0): 
        self.point_loads.append(PointLoad(float(x), float(P), float(angle_deg)))
        self._cached_solution = None

    def add_dist_load(self, x1, x2, shape, w0=0.0, expr="", angle_deg=0.0): 
        self.dist_loads.append(DistLoad(float(x1), float(x2), shape, float(w0), expr, float(angle_deg)))
        self._cached_solution = None

    def add_moment(self, x, M): 
        self.moments.append(AppliedMoment(float(x), float(M)))
        self._cached_solution = None

    def clear(self): 
        self.supports, self.point_loads, self.dist_loads, self.moments = [], [], [], []
        self._cached_solution = None

    def solve(self, n_points=2000):
        """Runs the 2D statics solver and caches the result."""
        if self._cached_solution is not None:
            return self._cached_solution

        v_unknowns, h_unknowns = [], []
        for s in self.supports:
            v_unknowns.append(("R", s))
            if s.kind == "Fixed": v_unknowns.append(("M", s))
            if s.kind in ("Pin", "Fixed"): h_unknowns.append(("Rx", s))

        if len(v_unknowns) != 2:
            raise StaticsError(f"Vertical subsystem needs exactly 2 unknowns (found {len(v_unknowns)}).")

        F_total_v, F_total_h, M_about_0 = 0.0, 0.0, 0.0

        for pl in self.point_loads:
            pv, ph = components(pl.P, pl.angle)
            F_total_v += pv; F_total_h += ph; M_about_0 += pv * pl.x

        dist_cache = []
        for dl in self.dist_loads:
            xs_s = np.linspace(dl.x1, dl.x2, 200)
            w_s = np.array([dl.w(xx) for xx in xs_s], dtype=float)
            wv_s, wh_s = components(w_s, dl.angle)
            F_total_v += _trapz(wv_s, xs_s)
            F_total_h += _trapz(wh_s, xs_s)
            M_about_0 += _trapz(wv_s * xs_s, xs_s)
            dist_cache.append((dl, xs_s, wv_s, wh_s))

        for m in self.moments: M_about_0 += m.M

        A = np.zeros((2, 2)); b = np.array([F_total_v, M_about_0], dtype=float)
        for i, (kind, s) in enumerate(v_unknowns):
            A[0, i] = 1.0 if kind == "R" else 0.0
            A[1, i] = s.x if kind == "R" else 1.0
        
        u = np.linalg.solve(A, b)
        reactions = []
        for (kind, s), val in zip(v_unknowns, u):
            existing = next((r for r in reactions if r["support"] is s), None)
            if not existing:
                existing = {"support": s, "R": 0.0, "Mr": 0.0, "Rx": 0.0}
                reactions.append(existing)
            if kind == "R": existing["R"] = val
            else: existing["Mr"] = val

        if len(h_unknowns) == 1:
            reactions[0]["Rx"] = F_total_h

        xs_all = [s.x for s in self.supports] + [pl.x for pl in self.point_loads] + [m.x for m in self.moments]
        for dl in self.dist_loads: xs_all += [dl.x1, dl.x2]
        L = max(xs_all) if xs_all else 1.0

        xs = np.linspace(0.0, L, n_points)
        dx = xs[1] - xs[0]

        point_events = []
        for r in reactions: point_events.append((r["support"].x, r["Rx"], r["R"], r["Mr"]))
        for pl in self.point_loads:
            pv, ph = components(pl.P, pl.angle)
            point_events.append((pl.x, -ph, -pv, 0.0))
        for m in self.moments: point_events.append((m.x, 0.0, 0.0, -m.M))

        applied_flags = [False] * len(point_events)
        N, V, M_diag = np.zeros_like(xs), np.zeros_like(xs), np.zeros_like(xs)
        n_, v_, mom = 0.0, 0.0, 0.0

        for i, x in enumerate(xs):
            for j, (ex, dN, dV, dM) in enumerate(point_events):
                if not applied_flags[j] and x >= ex - 1e-9:
                    n_ += dN; v_ += dV; mom += dM
                    applied_flags[j] = True
            for dl, xs_s, wv_s, wh_s in dist_cache:
                if dl.x1 < x <= dl.x2:
                    v_ -= np.interp(x, xs_s, wv_s) * dx
                    n_ -= np.interp(x, xs_s, wh_s) * dx
            N[i] = n_; V[i] = v_
            if i > 0: mom += (V[i - 1] + V[i]) / 2.0 * dx
            M_diag[i] = mom

        self._cached_solution = (reactions, xs, N, V, M_diag, L)
        return self._cached_solution

    # ----------------------------------------------------------------------
    # Data Querying Capabilities
    # ----------------------------------------------------------------------

    def get_reactions(self):
        """Returns and prints the reaction forces at all supports."""
        reactions, _, _, _, _, _ = self.solve()
        print("\n--- Support Reactions ---")
        for i, r in enumerate(reactions):
            print(f"Support {i+1} ({r['support'].kind}) @ x = {r['support'].x:.2f} m:")
            print(f"  R_y (Vertical)   = {r['R']:.2f} N")
            print(f"  R_x (Horizontal) = {r['Rx']:.2f} N")
            print(f"  M_r (Moment)     = {r['Mr']:.2f} N*m")
        return reactions

    def get_forces_at(self, x_val):
        """Returns the interpolated Axial, Shear, and Moment values at specific position x."""
        _, xs, N, V, M_diag, L = self.solve()
        
        if x_val < 0 or x_val > L:
            raise ValueError(f"Position x={x_val} is outside the beam span [0, {L}].")
        
        n_val = np.interp(x_val, xs, N)
        v_val = np.interp(x_val, xs, V)
        m_val = np.interp(x_val, xs, M_diag)
        
        print(f"\n--- Internal Forces @ x = {x_val:.2f} m ---")
        print(f"  Axial Force (N)   = {n_val:.2f} N")
        print(f"  Shear Force (V)   = {v_val:.2f} N")
        print(f"  Bending Moment (M)= {m_val:.2f} N*m")
        
        return {"x": x_val, "N": n_val, "V": v_val, "M": m_val}

    def get_extremes(self):
        """Identifies and returns the absolute maximum values for the entire beam."""
        _, xs, N, V, M_diag, _ = self.solve()
        
        # Max Absolute Values
        idx_N = np.argmax(np.abs(N))
        idx_V = np.argmax(np.abs(V))
        idx_M = np.argmax(np.abs(M_diag))

        extremes = {
            "Max_Axial": {"value": N[idx_N], "x": xs[idx_N]},
            "Max_Shear": {"value": V[idx_V], "x": xs[idx_V]},
            "Max_Moment": {"value": M_diag[idx_M], "x": xs[idx_M]},
        }

        print("\n--- Absolute Maximum Extreme Values ---")
        print(f"  Max Axial Force : {extremes['Max_Axial']['value']:.2f} N @ x = {extremes['Max_Axial']['x']:.2f} m")
        print(f"  Max Shear Force : {extremes['Max_Shear']['value']:.2f} N @ x = {extremes['Max_Shear']['x']:.2f} m")
        print(f"  Max Moment      : {extremes['Max_Moment']['value']:.2f} N*m @ x = {extremes['Max_Moment']['x']:.2f} m")
        
        return extremes

    def _setup_figure(self, title, figsize=(9, 4.5)):
        """Helper to construct styled unified clean layout containers."""
        fig, ax = plt.subplots(figsize=figsize)
        fig.patch.set_facecolor(self.panel_color)
        ax.set_facecolor(self.bg_color)
        ax.tick_params(colors=self.dim_color, labelsize=8)
        for sp in ax.spines.values(): sp.set_color(self.grid_color)
        ax.grid(True, color=self.grid_color, linewidth=0.8)
        for s in self.supports:
            ax.axvline(s.x, color=self.grid_color, lw=1.5, ls="--")
        return fig, ax

    # ----------------------------------------------------------------------
    # Isolated Plot Invocations
    # ----------------------------------------------------------------------

    def plot_schematic(self):
        """Displays a clean Free Body Diagram (FBD) including all forces and moments."""
        reactions, _, _, _, _, L = self.solve()
        fig, ax = self._setup_figure("Free Body Diagram", figsize=(10, 4))
        
        ax.axhline(0, color=self.ink_color, lw=4, zorder=2)
        ax.set_xlim(-1.0, L + 1.0)
        ax.set_ylim(-2.0, 2.0)
        ax.set_yticks([])
        ax.set_title("Proper Free Body Diagram (FBD)", color=self.ink_color, fontsize=12, loc="left", fontweight="bold")

        def draw_moment(x, M, color, label, y_offset=0.0):
            if abs(M) < 1e-9: return
            direction = 0.4 if M > 0 else -0.4
            start_x, end_x = x + 0.4, x - 0.4
            if M < 0: start_x, end_x = x - 0.4, x + 0.4
            
            ax.annotate("", xy=(end_x, y_offset + 0.3), xytext=(start_x, y_offset + 0.3),
                        arrowprops=dict(arrowstyle="-|>", connectionstyle=f"arc3,rad={direction}", color=color, lw=1.5), zorder=3)
            ax.text(x, y_offset + 0.7, label, color=color, fontsize=9, ha="center")

        for r in reactions:
            s = r["support"]
            if abs(r['R']) > 1e-9:
                dy = -1.0 if r['R'] > 0 else 1.0
                ax.annotate("", xy=(s.x, 0), xytext=(s.x, dy),
                            arrowprops=dict(arrowstyle="-|>", color=self.amber_color, lw=2), zorder=3)
                ax.text(s.x, dy + (-0.2 if dy < 0 else 0.2), fr"$R_y = {r['R']:.1f}$", color=self.amber_color, fontsize=9, ha="center", fontweight="bold")
            
            if abs(r['Rx']) > 1e-9:
                dx = -1.0 if r['Rx'] > 0 else 1.0
                ax.annotate("", xy=(s.x, 0), xytext=(s.x + dx, 0),
                            arrowprops=dict(arrowstyle="-|>", color=self.amber_color, lw=2), zorder=3)
                ax.text(s.x + dx, -0.3, fr"$R_x = {r['Rx']:.1f}$", color=self.amber_color, fontsize=9, ha="center", fontweight="bold")

            draw_moment(s.x, r.get('Mr', 0.0), self.amber_color, fr"$M_r = {r.get('Mr', 0.0):.1f}$")

        for pl in self.point_loads:
            pv, ph = components(pl.P, pl.angle)
            dy = 1.0 if pv >= 0 else -1.0 
            ax.annotate("", xy=(pl.x, 0), xytext=(pl.x, dy),
                        arrowprops=dict(arrowstyle="-|>", color=self.teal_color, lw=2), zorder=3)
            ax.text(pl.x, dy + (0.2 if dy > 0 else -0.2), fr"$P = {pl.P:.0f}$", color=self.teal_color, fontsize=9, ha="center", fontweight="bold")

        for m in self.moments:
            draw_moment(m.x, m.M, self.teal_color, fr"$M = {m.M:.1f}$")

        for dl in self.dist_loads:
            num_arrows = max(4, int((dl.x2 - dl.x1) * 3))
            xs = np.linspace(dl.x1, dl.x2, num_arrows)
            eff_v, _ = components(dl.w0, dl.angle)
            dy_top = 0.8 if eff_v >= 0 else -0.8
            
            ax.plot([dl.x1, dl.x2], [dy_top, dy_top], color=self.red_color, lw=1.5)
            
            for xf in xs:
                ax.annotate("", xy=(xf, 0), xytext=(xf, dy_top),
                            arrowprops=dict(arrowstyle="-|>", color=self.red_color, lw=1), zorder=3)
            
            text_y = dy_top + (0.2 if dy_top > 0 else -0.3)
            ax.text((dl.x1 + dl.x2) / 2, text_y, dl.label(), color=self.red_color, fontsize=9, ha="center", fontweight="bold")

        plt.show()

    def plot_axial(self):
        """Displays purely the Axial Force Diagram N(x)."""
        _, xs, N, _, _, _ = self.solve()
        fig, ax = self._setup_figure(r"Axial Force Diagram $N(x)$")
        ax.axhline(0, color=self.ink_color, lw=1.5)
        ax.plot(xs, N, color=self.purple_color, lw=2)
        ax.fill_between(xs, N, 0, color=self.purple_color, alpha=0.15)
        ax.set_ylabel(r"Axial Force $N$ (N)", color=self.dim_color, fontsize=10)
        ax.set_title(r"Axial Force Diagram $N(x)$", color=self.ink_color, fontsize=12, loc="left", fontweight="bold")
        plt.show()

    def plot_shear(self):
        """Displays purely the Shear Force Diagram V(x)."""
        _, xs, _, V, _, _ = self.solve()
        fig, ax = self._setup_figure(r"Shear Diagram $V(x)$")
        ax.axhline(0, color=self.ink_color, lw=1.5)
        ax.plot(xs, V, color=self.teal_color, lw=2)
        ax.fill_between(xs, V, 0, color=self.teal_color, alpha=0.15)
        ax.set_ylabel(r"Shear Force $V$ (N)", color=self.dim_color, fontsize=10)
        ax.set_title(r"Shear Force Diagram $V(x)$", color=self.ink_color, fontsize=12, loc="left", fontweight="bold")
        plt.show()

    def plot_moment(self):
        """Displays purely the Bending Moment Diagram M(x)."""
        _, xs, _, _, M_diag, _ = self.solve()
        fig, ax = self._setup_figure(r"Moment Diagram $M(x)$")
        ax.axhline(0, color=self.ink_color, lw=1.5)
        ax.plot(xs, M_diag, color=self.amber_color, lw=2)
        ax.fill_between(xs, M_diag, 0, color=self.amber_color, alpha=0.15)
        ax.set_xlabel(r"Position $x$ (m)", color=self.dim_color, fontsize=10)
        ax.set_ylabel(r"Bending Moment $M$ (N$\cdot$m)", color=self.dim_color, fontsize=10)
        ax.set_title(r"Bending Moment Diagram $M(x)$", color=self.ink_color, fontsize=12, loc="left", fontweight="bold")
        
        if len(M_diag):
            idx_max = int(np.argmax(np.abs(M_diag)))
            ax.annotate(fr"$M_{{max}} = {M_diag[idx_max]:.1f}$ N$\cdot$m @ $x={xs[idx_max]:.2f}$ m",
                               xy=(xs[idx_max], M_diag[idx_max]), color=self.amber_color, fontsize=9,
                               fontweight="bold", xytext=(10, 10), textcoords="offset points")
        plt.show()


# ----------------------------------------------------------------------
# Usage Execution Example
# ----------------------------------------------------------------------
if __name__ == "__main__":
    beam = BeamStudio()

    # Define Supports
    beam.add_support("Pin", x=0.0)      
    beam.add_support("Roller", x=(45+200+45))

    # Distributed load: 5200 N/m over 200 m (uniform)
    beam.add_dist_load(x1=(45), x2=(45+200), shape="uniform", w0=5200, angle_deg=180)  

    # Point load
    beam.add_point_load(x=(45+200+45+70), P=201.88, angle_deg=0)  

    # ---------------------------------------------------------
    # 1. Querying Exact Values (New Features)
    # ---------------------------------------------------------
    
    # Pre-solve to cache the solution (optional, methods will auto-trigger it)
    beam.solve() 

    # A. Get Reaction Solutions
    reactions = beam.get_reactions()

    # B. Get values at a specific point (e.g., exactly at x = 100)
    forces_at_100 = beam.get_forces_at(x_val=100.0)

    # C. Get all extreme cases (Max Shear, Max Moment, Max Axial)
    extremes = beam.get_extremes()

    # ---------------------------------------------------------
    # 2. Plotting (Existing Features)
    # ---------------------------------------------------------
    beam.plot_schematic()
    beam.plot_shear()
    beam.plot_moment()