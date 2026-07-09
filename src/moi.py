import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon as MplPolygon


def compute_properties(shapes):
    """shapes: list of point-lists. First = solid outline (CCW). Rest = holes (CW)."""
    A_total = Qx_total = Qy_total = 0.0
    Ixx_o = Iyy_o = Ixy_o = 0.0

    for verts in shapes:
        verts = np.asarray(verts, dtype=float)
        x, y = verts[:, 0], verts[:, 1]
        x1, y1 = np.roll(x, -1), np.roll(y, -1)
        cross = x * y1 - x1 * y

        A = np.sum(cross) / 2.0
        Qx = np.sum((y + y1) * cross) / 6.0
        Qy = np.sum((x + x1) * cross) / 6.0
        Ixx = np.sum((y**2 + y*y1 + y1**2) * cross) / 12.0
        Iyy = np.sum((x**2 + x*x1 + x1**2) * cross) / 12.0
        Ixy = np.sum((x*y1 + 2*x*y + 2*x1*y1 + x1*y) * cross) / 24.0

        A_total += A
        Qx_total += Qx
        Qy_total += Qy
        Ixx_o += Ixx
        Iyy_o += Iyy
        Ixy_o += Ixy

    if A_total <= 0:
        raise ValueError("Area <= 0. Solid must be CCW, holes CW.")

    cx = Qy_total / A_total
    cy = Qx_total / A_total

    Ixx = Ixx_o - A_total * cy**2
    Iyy = Iyy_o - A_total * cx**2
    Ixy = Ixy_o - A_total * cx * cy
    J = Ixx + Iyy

    all_pts = np.concatenate([np.asarray(s) for s in shapes])
    c_top = all_pts[:, 1].max() - cy
    c_bottom = cy - all_pts[:, 1].min()
    c_right = all_pts[:, 0].max() - cx
    c_left = cx - all_pts[:, 0].min()

    return {
        "area": A_total, "centroid": (cx, cy),
        "Ixx": Ixx, "Iyy": Iyy, "Ixy": Ixy, "J": J,
        "rx": np.sqrt(Ixx / A_total), "ry": np.sqrt(Iyy / A_total),
        "c_top": c_top, "c_bottom": c_bottom,
        "Sx_top": Ixx / c_top if c_top > 0 else float("inf"),
        "Sx_bottom": Ixx / c_bottom if c_bottom > 0 else float("inf"),
        "c_left": c_left, "c_right": c_right,
        "Sy_left": Iyy / c_left if c_left > 0 else float("inf"),
        "Sy_right": Iyy / c_right if c_right > 0 else float("inf"),
    }


# ---------- shape generators ----------

def rectangle(w, h, origin=(0, 0)):
    ox, oy = origin
    return [(ox, oy), (ox+w, oy), (ox+w, oy+h), (ox, oy+h)]

def triangle(b, h, origin=(0, 0)):
    ox, oy = origin
    return [(ox, oy), (ox+b, oy), (ox+b/2, oy+h)]

def circle(d, center=(0, 0), n=200):
    r = d / 2
    cx, cy = center
    t = np.linspace(0, 2*np.pi, n, endpoint=False)
    return list(zip(cx + r*np.cos(t), cy + r*np.sin(t)))

def hollow_circle(d_out, d_in, center=(0, 0), n=200):
    outer = circle(d_out, center, n)
    inner = circle(d_in, center, n)[::-1]  # reversed = hole
    return [outer, inner]

def i_beam(depth, bf, tf, tw, origin=(0, 0)):
    ox, oy = origin
    x0, x1, x2, x3 = ox, ox+(bf-tw)/2, ox+(bf+tw)/2, ox+bf
    y0, y1, y2, y3 = oy, oy+tf, oy+depth-tf, oy+depth
    return [(x0,y0),(x3,y0),(x3,y1),(x2,y1),(x2,y2),(x3,y2),
            (x3,y3),(x0,y3),(x0,y2),(x1,y2),(x1,y1),(x0,y1)]

def l_angle(h, w, t, origin=(0, 0)):
    ox, oy = origin
    return [(ox,oy),(ox+w,oy),(ox+w,oy+t),(ox+t,oy+t),(ox+t,oy+h),(ox,oy+h)]

def custom_polygon(points):
    return list(points)


# ---------- DISPLAY ----------

def show_shape(shapes, props=None, title="Section", show_dims=True, save_path=None):
    """shapes: list of point-lists (first = outline, rest = holes)."""
    if props is None:
        props = compute_properties(shapes)

    fig, ax = plt.subplots(figsize=(6, 6))

    for i, verts in enumerate(shapes):
        verts = np.asarray(verts, dtype=float)
        is_hole = i > 0
        ax.add_patch(MplPolygon(
            verts, closed=True,
            facecolor="white" if is_hole else "#bee3f8",
            edgecolor="#2b6cb0", linewidth=2,
        ))
        ax.plot(verts[:, 0], verts[:, 1], "o", color="#2b6cb0", markersize=3)

    cx, cy = props["centroid"]
    ax.plot(cx, cy, "+", color="crimson", markersize=16, markeredgewidth=2.5, label="Centroid")

    all_pts = np.concatenate([np.asarray(s) for s in shapes])
    xmin, xmax = all_pts[:, 0].min(), all_pts[:, 0].max()
    ymin, ymax = all_pts[:, 1].min(), all_pts[:, 1].max()
    pad = 0.12 * max(xmax - xmin, ymax - ymin)

    if show_dims:
        ax.plot([xmin - pad*0.3, xmax + pad*0.3], [cy, cy], "--", color="gray", linewidth=1)
        ax.plot([cx, cx], [ymin - pad*0.3, ymax + pad*0.3], "--", color="gray", linewidth=1)

    ax.set_xlim(xmin - pad, xmax + pad)
    ax.set_ylim(ymin - pad, ymax + pad)
    ax.set_aspect("equal")
    ax.grid(alpha=0.3)
    ax.legend(loc="upper right")
    ax.set_title(
        f"{title}\n"
        f"A={props['area']:.4g}   centroid=({cx:.3g}, {cy:.3g})\n"
        f"Ixx={props['Ixx']:.4g}   Iyy={props['Iyy']:.4g}   J={props['J']:.4g}",
        fontsize=10,
    )
    fig.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=150)

    return fig

def area(shapes):
    return compute_properties(shapes)["area"]

def centroid(shapes):
    return compute_properties(shapes)["centroid"]

def moment_of_inertia(shapes):
    props = compute_properties(shapes)
    return props["Ixx"], props["Iyy"], props["Ixy"], props["J"]

def section_modulus(shapes):
    props = compute_properties(shapes)
    return props["Sx_top"], props["Sx_bottom"], props["Sy_left"], props["Sy_right"]

def radius_of_gyration(shapes):
    props = compute_properties(shapes)
    return props["rx"], props["ry"]

def extreme_fiber_distance(shapes):
    props = compute_properties(shapes)
    return props["c_top"], props["c_bottom"], props["c_left"], props["c_right"]

if __name__ == "__main__":
    # I-beam
    verts = i_beam(depth=20, bf=10, tf=1.5, tw=0.8)
    show_shape([verts], title="I-Beam", save_path="ibeam.png")

    # hollow tube (has a hole)
    shapes = hollow_circle(d_out=8, d_in=5)
    show_shape(shapes, title="Hollow Tube", save_path="tube.png")

    # fully custom shape
    my_shape = custom_polygon([(0,0), (5,0), (5,3), (2,3), (2,6), (0,6)])
    show_shape([my_shape], title="Custom Shape", save_path="custom.png")

    plt.show()  # pops up windows if running locally (not needed if just saving files)

    print(f"Area of I-beam: {area([verts]):.4g}")
    print(f"Centroid of I-beam: {centroid([verts])}")
    print(f"Moments of inertia of I-beam: {moment_of_inertia([verts])}")
    print(f"Section moduli of I-beam: {section_modulus([verts])}")
    print(f"Radius of gyration of I-beam: {radius_of_gyration([verts])}")
    print(f"Extreme fiber distances of I-beam: {extreme_fiber_distance([verts])}")
