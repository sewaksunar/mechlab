"""Unified animation framework for MechLab.

Provides a single, extensible animation system that works with ANY
physics object implementing the Animatable protocol.

Architecture:
  - BaseAnimator: Core animation logic (backend handling, export)
  - PlotPanel: Reusable subplot configurations
  - AnimatorFactory: Auto-creates appropriate animator for any object

Benefits:
  - Zero code duplication across different physics animations
  - Consistent API for all object types
  - Easy to add new visualization panels
  - Automatic backend handling for export
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Protocol,
    Tuple,
    Type,
    Union,
    runtime_checkable,
)

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.figure import Figure
from matplotlib.axes import Axes

from mechlab.core.base import (
    Animatable,
    PhysicsState,
    animation_registry,
    config,
)


# =============================================================================
# PLOT PANEL SYSTEM - Reusable subplot components
# =============================================================================

@dataclass
class PlotPanel:
    """Configuration for a single subplot panel.

    Defines what data to show and how to display it.
    Panels are composable building blocks for animations.
    """
    name: str
    title: str
    xlabel: str = ""
    ylabel: str = ""
    aspect: Optional[str] = None  # "equal", "auto", None
    grid: bool = True
    legend: bool = True

    # Data configuration
    x_key: str = "x"  # Key in data dict for x-axis
    y_key: str = "y"  # Key in data dict for y-axis

    # Style
    static_style: Dict[str, Any] = field(default_factory=lambda: {"linestyle": "--", "alpha": 0.5})
    animated_style: Dict[str, Any] = field(default_factory=lambda: {"marker": "o", "markersize": 8})


# Pre-defined panel configurations
TRAJECTORY_PANEL = PlotPanel(
    name="trajectory",
    title="Trajectory",
    xlabel="Horizontal Distance (m)",
    ylabel="Height (m)",
    aspect="equal",
    x_key="pos_x",
    y_key="pos_y",
)

VELOCITY_PANEL = PlotPanel(
    name="velocity",
    title="Velocity Components",
    xlabel="Time (s)",
    ylabel="Velocity (m/s)",
)

ENERGY_PANEL = PlotPanel(
    name="energy",
    title="Energy Analysis",
    xlabel="Time (s)",
    ylabel="Energy (J)",
)

STATE_PANEL = PlotPanel(
    name="state",
    title="Current State",
    xlabel="",
    ylabel="",
    grid=False,
    legend=False,
)


# =============================================================================
# BASE ANIMATOR
# =============================================================================

class BaseAnimator(ABC):
    """Base class for all animators.

    Handles:
      - Figure/axes setup with proper backend management
      - Animation creation and control
      - Export to MP4, GIF, PNG with automatic backend switching
      - Consistent styling and layout

    Subclasses implement:
      - _setup_panels(): Configure subplots
      - _init_animation(): Initialize animated elements
      - _update_frame(): Update for each frame
    """

    def __init__(
        self,
        obj: Animatable,
        figsize: Tuple[float, float] = (14, 10),
        dpi: int = 100,
        num_points: int = 200,
    ) -> None:
        """Initialize animator.

        Args:
            obj: Any object implementing Animatable protocol
            figsize: Figure size (width, height) in inches
            dpi: Display resolution
            num_points: Number of trajectory points
        """
        self.obj = obj
        self.figsize = figsize
        self.dpi = dpi
        self.num_points = num_points

        # Get animation data from object
        self.t_array, self.positions, self.velocities = obj.trajectory(num_points)
        self._compute_derived_data()

        # Setup figure (interactive mode)
        self._setup_figure()

    def _compute_derived_data(self) -> None:
        """Compute derived quantities (energy, etc.). Override in subclasses."""
        pass

    @abstractmethod
    def _setup_figure(self) -> None:
        """Create figure with subplots. Must set self.fig and self.axes."""
        pass

    @abstractmethod
    def _init_animation(self) -> tuple:
        """Initialize all animated elements. Return tuple of artists."""
        pass

    @abstractmethod
    def _update_frame(self, frame: int) -> tuple:
        """Update all elements for given frame. Return tuple of artists."""
        pass

    def preview(self) -> None:
        """Display interactive animation."""
        ani = FuncAnimation(
            self.fig,
            self._update_frame,
            frames=range(len(self.t_array)),
            init_func=self._init_animation,
            interval=30,
            blit=True,
            repeat=True,
        )
        plt.show()

    def _create_export_figure(self) -> Tuple[Figure, Any]:
        """Create a new figure for export with Agg backend.

        Returns:
            (figure, axes_dict) for export
        """
        # This must be implemented by subclasses to recreate their specific layout
        raise NotImplementedError

    def save_mp4(
        self,
        filename: str = "animation.mp4",
        fps: int = 30,
    ) -> None:
        """Save animation as MP4."""
        self._save_animation(filename, fps, writer=config.mp4_writer)

    def save_gif(
        self,
        filename: str = "animation.gif",
        fps: int = 20,
    ) -> None:
        """Save animation as GIF."""
        self._save_animation(filename, fps, writer=config.gif_writer)

    def _save_animation(
        self,
        filename: str,
        fps: int,
        writer: str,
    ) -> None:
        """Internal method to save animation with proper backend handling."""
        old_backend = matplotlib.get_backend()
        matplotlib.use("Agg", force=True)

        try:
            fig, init_func, update_func = self._create_export_animation()

            ani = FuncAnimation(
                fig,
                update_func,
                frames=range(len(self.t_array)),
                init_func=init_func,
                blit=True,
            )
            ani.save(filename, fps=fps, writer=writer)
            plt.close(fig)
            print(f"✔ Saved: {filename}")
        finally:
            matplotlib.use(old_backend, force=True)

    @abstractmethod
    def _create_export_animation(self) -> Tuple[Figure, Callable, Callable]:
        """Create figure and callbacks for export.

        Returns:
            (fig, init_func, update_func)
        """
        pass

    def save_snapshot(
        self,
        filename: str = "snapshot.png",
        frame: int = 0,
        dpi: int = 150,
    ) -> None:
        """Save single frame as image."""
        self._init_animation()
        self._update_frame(frame)
        self.fig.savefig(filename, dpi=dpi, bbox_inches="tight")
        print(f"✔ Saved: {filename}")


# =============================================================================
# PHYSICS ANIMATOR - Generic animator for PhysicsObject subclasses
# =============================================================================

class PhysicsAnimator(BaseAnimator):
    """Generic animator for any PhysicsObject.

    Creates a standard 2x2 layout:
      - Trajectory (upper left)
      - Velocity components (upper right)
      - Energy analysis (lower left)
      - State info (lower right)

    Works automatically with any class implementing:
      - trajectory() -> (t_array, positions, velocities)
      - time_span() -> (t_start, t_end)
      - kinetic_energy() (optional)
      - mass attribute (optional, for energy)
    """

    def __init__(
        self,
        obj: Animatable,
        g: float = 9.81,
        **kwargs: Any,
    ) -> None:
        self.g = g
        super().__init__(obj, **kwargs)

    def _compute_derived_data(self) -> None:
        """Compute kinetic and potential energy arrays."""
        mass = getattr(self.obj, "mass", 1.0)

        # Kinetic energy
        self.ke_array = np.array([
            0.5 * mass * np.linalg.norm(v) ** 2
            for v in self.velocities
        ])

        # Potential energy (relative to starting height)
        y0 = self.positions[0, 1] if len(self.positions) > 0 else 0
        self.pe_array = np.array([
            mass * self.g * (pos[1] - y0)
            for pos in self.positions
        ])

        self.total_energy = self.ke_array + self.pe_array

    def _setup_figure(self) -> None:
        """Create 2x2 subplot layout."""
        self.fig = plt.figure(figsize=self.figsize, dpi=self.dpi)
        self.fig.suptitle(
            f"{self.obj.__class__.__name__} Animation",
            fontsize=16,
            fontweight="bold",
        )

        gs = self.fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)

        # Trajectory
        self.ax_traj = self.fig.add_subplot(gs[0, 0])
        self._setup_trajectory_axes(self.ax_traj)

        # Velocity
        self.ax_vel = self.fig.add_subplot(gs[0, 1])
        self._setup_velocity_axes(self.ax_vel)

        # Energy
        self.ax_energy = self.fig.add_subplot(gs[1, 0])
        self._setup_energy_axes(self.ax_energy)

        # State text
        self.ax_text = self.fig.add_subplot(gs[1, 1])
        self._setup_text_axes(self.ax_text)

    def _setup_trajectory_axes(self, ax: Axes) -> None:
        """Configure trajectory subplot."""
        ax.set_xlabel("Horizontal Distance (m)", fontsize=10)
        ax.set_ylabel("Height (m)", fontsize=10)
        ax.set_title("Trajectory", fontweight="bold")
        ax.grid(True, alpha=0.3)
        ax.set_aspect("equal", adjustable="box")

        # Static path
        ax.plot(
            self.positions[:, 0],
            self.positions[:, 1],
            "b--", alpha=0.5, lw=1, label="Path",
        )

        # Animated elements
        self.traj_point, = ax.plot([], [], "ro", ms=10, label="Current")
        ax.legend(loc="upper right", fontsize=9)

    def _setup_velocity_axes(self, ax: Axes) -> None:
        """Configure velocity subplot."""
        ax.set_xlabel("Time (s)", fontsize=10)
        ax.set_ylabel("Velocity (m/s)", fontsize=10)
        ax.set_title("Velocity Components", fontweight="bold")
        ax.grid(True, alpha=0.3)

        # Static curves
        ax.plot(self.t_array, self.velocities[:, 0], "r-", lw=1.5, label="$v_x$")
        ax.plot(self.t_array, self.velocities[:, 1], "g-", lw=1.5, label="$v_y$")
        ax.plot(self.t_array, self.velocities[:, 2], "b-", lw=1.5, label="$v_z$")

        # Animated points
        self.vel_pt_x, = ax.plot([], [], "ro", ms=6)
        self.vel_pt_y, = ax.plot([], [], "go", ms=6)
        self.vel_pt_z, = ax.plot([], [], "bo", ms=6)
        ax.legend(loc="best", fontsize=9)

    def _setup_energy_axes(self, ax: Axes) -> None:
        """Configure energy subplot."""
        ax.set_xlabel("Time (s)", fontsize=10)
        ax.set_ylabel("Energy (J)", fontsize=10)
        ax.set_title("Energy Analysis", fontweight="bold")
        ax.grid(True, alpha=0.3)

        # Static curves
        ax.plot(self.t_array, self.ke_array, "r-", lw=1.5, label="KE")
        ax.plot(self.t_array, self.pe_array, "b-", lw=1.5, label="PE")
        ax.plot(self.t_array, self.total_energy, "k--", lw=1.5, label="Total")

        # Animated points
        self.energy_pt_ke, = ax.plot([], [], "ro", ms=6)
        self.energy_pt_pe, = ax.plot([], [], "bo", ms=6)
        self.energy_pt_total, = ax.plot([], [], "ko", ms=6)
        ax.legend(loc="best", fontsize=9)

    def _setup_text_axes(self, ax: Axes) -> None:
        """Configure state text subplot."""
        ax.axis("off")
        self.text_display = ax.text(
            0.05, 0.95, "",
            transform=ax.transAxes,
            fontfamily="monospace",
            fontsize=9,
            verticalalignment="top",
            bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5),
        )

    def _init_animation(self) -> tuple:
        """Initialize animated elements."""
        self.traj_point.set_data([], [])
        self.vel_pt_x.set_data([], [])
        self.vel_pt_y.set_data([], [])
        self.vel_pt_z.set_data([], [])
        self.energy_pt_ke.set_data([], [])
        self.energy_pt_pe.set_data([], [])
        self.energy_pt_total.set_data([], [])
        self.text_display.set_text("")
        return (
            self.traj_point, self.vel_pt_x, self.vel_pt_y, self.vel_pt_z,
            self.energy_pt_ke, self.energy_pt_pe, self.energy_pt_total,
            self.text_display,
        )

    def _update_frame(self, frame: int) -> tuple:
        """Update all elements for frame."""
        frame = min(frame, len(self.t_array) - 1)

        t = self.t_array[frame]
        pos = self.positions[frame]
        vel = self.velocities[frame]
        ke = self.ke_array[frame]
        pe = self.pe_array[frame]
        e_total = self.total_energy[frame]

        # Update trajectory
        self.traj_point.set_data([pos[0]], [pos[1]])

        # Update velocity points
        self.vel_pt_x.set_data([t], [vel[0]])
        self.vel_pt_y.set_data([t], [vel[1]])
        self.vel_pt_z.set_data([t], [vel[2]])

        # Update energy points
        self.energy_pt_ke.set_data([t], [ke])
        self.energy_pt_pe.set_data([t], [pe])
        self.energy_pt_total.set_data([t], [e_total])

        # Update text
        v_mag = np.linalg.norm(vel)
        mass = getattr(self.obj, "mass", 1.0)
        text = (
            f"Time: {t:.3f} s\n\n"
            f"Position:\n"
            f"  x = {pos[0]:>8.3f} m\n"
            f"  y = {pos[1]:>8.3f} m\n"
            f"  z = {pos[2]:>8.3f} m\n\n"
            f"Velocity:\n"
            f"  vx = {vel[0]:>7.3f} m/s\n"
            f"  vy = {vel[1]:>7.3f} m/s\n"
            f"  vz = {vel[2]:>7.3f} m/s\n"
            f"  |v| = {v_mag:>7.3f} m/s\n\n"
            f"Energy:\n"
            f"  KE = {ke:>7.3f} J\n"
            f"  PE = {pe:>7.3f} J\n"
            f"  Total = {e_total:>7.3f} J\n\n"
            f"Parameters:\n"
            f"  mass = {mass:.3f} kg\n"
            f"  g = {self.g:.3f} m/s²"
        )
        self.text_display.set_text(text)

        return (
            self.traj_point, self.vel_pt_x, self.vel_pt_y, self.vel_pt_z,
            self.energy_pt_ke, self.energy_pt_pe, self.energy_pt_total,
            self.text_display,
        )

    def _create_export_animation(self) -> Tuple[Figure, Callable, Callable]:
        """Create fresh figure for export."""
        fig = plt.figure(figsize=self.figsize, dpi=self.dpi)
        fig.suptitle(
            f"{self.obj.__class__.__name__} Animation",
            fontsize=16,
            fontweight="bold",
        )

        gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)

        # Trajectory
        ax_traj = fig.add_subplot(gs[0, 0])
        ax_traj.set_xlabel("Horizontal Distance (m)", fontsize=10)
        ax_traj.set_ylabel("Height (m)", fontsize=10)
        ax_traj.set_title("Trajectory", fontweight="bold")
        ax_traj.grid(True, alpha=0.3)
        ax_traj.set_aspect("equal", adjustable="box")
        ax_traj.plot(self.positions[:, 0], self.positions[:, 1], "b--", alpha=0.5, lw=1)
        traj_point, = ax_traj.plot([], [], "ro", ms=10)

        # Velocity
        ax_vel = fig.add_subplot(gs[0, 1])
        ax_vel.set_xlabel("Time (s)", fontsize=10)
        ax_vel.set_ylabel("Velocity (m/s)", fontsize=10)
        ax_vel.set_title("Velocity Components", fontweight="bold")
        ax_vel.grid(True, alpha=0.3)
        ax_vel.plot(self.t_array, self.velocities[:, 0], "r-", lw=1.5, label="$v_x$")
        ax_vel.plot(self.t_array, self.velocities[:, 1], "g-", lw=1.5, label="$v_y$")
        ax_vel.plot(self.t_array, self.velocities[:, 2], "b-", lw=1.5, label="$v_z$")
        vel_pt_x, = ax_vel.plot([], [], "ro", ms=6)
        vel_pt_y, = ax_vel.plot([], [], "go", ms=6)
        vel_pt_z, = ax_vel.plot([], [], "bo", ms=6)
        ax_vel.legend(loc="best", fontsize=9)

        # Energy
        ax_energy = fig.add_subplot(gs[1, 0])
        ax_energy.set_xlabel("Time (s)", fontsize=10)
        ax_energy.set_ylabel("Energy (J)", fontsize=10)
        ax_energy.set_title("Energy Analysis", fontweight="bold")
        ax_energy.grid(True, alpha=0.3)
        ax_energy.plot(self.t_array, self.ke_array, "r-", lw=1.5, label="KE")
        ax_energy.plot(self.t_array, self.pe_array, "b-", lw=1.5, label="PE")
        ax_energy.plot(self.t_array, self.total_energy, "k--", lw=1.5, label="Total")
        energy_pt_ke, = ax_energy.plot([], [], "ro", ms=6)
        energy_pt_pe, = ax_energy.plot([], [], "bo", ms=6)
        energy_pt_total, = ax_energy.plot([], [], "ko", ms=6)
        ax_energy.legend(loc="best", fontsize=9)

        # Text
        ax_text = fig.add_subplot(gs[1, 1])
        ax_text.axis("off")
        text_display = ax_text.text(
            0.05, 0.95, "",
            transform=ax_text.transAxes,
            fontfamily="monospace",
            fontsize=9,
            verticalalignment="top",
            bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5),
        )

        def init():
            traj_point.set_data([], [])
            vel_pt_x.set_data([], [])
            vel_pt_y.set_data([], [])
            vel_pt_z.set_data([], [])
            energy_pt_ke.set_data([], [])
            energy_pt_pe.set_data([], [])
            energy_pt_total.set_data([], [])
            text_display.set_text("")
            return (traj_point, vel_pt_x, vel_pt_y, vel_pt_z,
                    energy_pt_ke, energy_pt_pe, energy_pt_total, text_display)

        def update(frame):
            frame = min(frame, len(self.t_array) - 1)
            t = self.t_array[frame]
            pos = self.positions[frame]
            vel = self.velocities[frame]
            ke = self.ke_array[frame]
            pe = self.pe_array[frame]
            e_total = self.total_energy[frame]

            traj_point.set_data([pos[0]], [pos[1]])
            vel_pt_x.set_data([t], [vel[0]])
            vel_pt_y.set_data([t], [vel[1]])
            vel_pt_z.set_data([t], [vel[2]])
            energy_pt_ke.set_data([t], [ke])
            energy_pt_pe.set_data([t], [pe])
            energy_pt_total.set_data([t], [e_total])

            v_mag = np.linalg.norm(vel)
            mass = getattr(self.obj, "mass", 1.0)
            text = (
                f"Time: {t:.3f} s\n\n"
                f"Position:\n"
                f"  x = {pos[0]:>8.3f} m\n"
                f"  y = {pos[1]:>8.3f} m\n"
                f"  z = {pos[2]:>8.3f} m\n\n"
                f"Velocity:\n"
                f"  vx = {vel[0]:>7.3f} m/s\n"
                f"  vy = {vel[1]:>7.3f} m/s\n"
                f"  vz = {vel[2]:>7.3f} m/s\n"
                f"  |v| = {v_mag:>7.3f} m/s\n\n"
                f"Energy:\n"
                f"  KE = {ke:>7.3f} J\n"
                f"  PE = {pe:>7.3f} J\n"
                f"  Total = {e_total:>7.3f} J\n\n"
                f"Parameters:\n"
                f"  mass = {mass:.3f} kg\n"
                f"  g = {self.g:.3f} m/s²"
            )
            text_display.set_text(text)

            return (traj_point, vel_pt_x, vel_pt_y, vel_pt_z,
                    energy_pt_ke, energy_pt_pe, energy_pt_total, text_display)

        return fig, init, update


# =============================================================================
# ANIMATOR FACTORY - Auto-select appropriate animator
# =============================================================================

def animate(obj: Any, **kwargs: Any) -> BaseAnimator:
    """Factory function to create appropriate animator for any object.

    Automatically selects the best animator based on object type.
    This is the main entry point for animations.

    Args:
        obj: Any animatable object
        **kwargs: Passed to animator constructor

    Returns:
        Appropriate animator instance

    Example:
        >>> from mechlab.mechanics.dynamics import Projectile
        >>> from mechlab.visual import animate
        >>> proj = Projectile(velocity=(20, 20, 0))
        >>> anim = animate(proj)
        >>> anim.preview()
    """
    # Check if object has custom animator registered
    obj_class = obj.__class__.__name__

    if obj_class in animation_registry:
        animator_class = animation_registry.get(obj_class)
        return animator_class(obj, **kwargs)

    # Check if object implements Animatable protocol
    if isinstance(obj, Animatable):
        return PhysicsAnimator(obj, **kwargs)

    raise TypeError(
        f"Object of type {obj_class} is not animatable. "
        f"It must implement the Animatable protocol (trajectory() and time_span() methods)."
    )


# =============================================================================
# PROJECTION UTILITIES (merged from projection.py)
# =============================================================================

class Projection:
    """Project 3D points into 2D using orthographic or perspective modes.

    Useful for rendering 3D objects in 2D animations.

    Args:
        mode: 'orthographic' or 'perspective'
        fov: field of view in degrees (perspective only)
        distance: viewer distance from origin (perspective only)

    Example:
        >>> proj = Projection(mode="perspective", distance=6.0)
        >>> pts_2d = proj.project_rotated(vertices, angles=(30, 45, 0))
    """

    def __init__(
        self,
        mode: str = "orthographic",
        fov: float = 60.0,
        distance: float = 5.0,
    ) -> None:
        self.mode = mode
        self.fov = float(fov)
        self.distance = float(distance)

    @staticmethod
    def _rotation_matrix(rx: float, ry: float, rz: float) -> np.ndarray:
        """Return combined rotation matrix for rotations (radians) about x,y,z."""
        cx, sx = np.cos(rx), np.sin(rx)
        cy, sy = np.cos(ry), np.sin(ry)
        cz, sz = np.cos(rz), np.sin(rz)

        Rx = np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]])
        Ry = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]])
        Rz = np.array([[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]])

        return Rz @ Ry @ Rx

    def rotate(self, points: np.ndarray, angles: tuple[float, ...]) -> np.ndarray:
        """Rotate points by angles (degrees) around x,y,z.

        Args:
            points: (N,3) array
            angles: (rx, ry, rz) in degrees

        Returns:
            rotated (N,3) array
        """
        rx, ry, rz = np.radians(angles)
        R = self._rotation_matrix(rx, ry, rz)
        return (R @ points.T).T

    def project(self, points: np.ndarray) -> np.ndarray:
        """Project (N,3) points to (N,2).

        For perspective projection the camera is located at z = -distance
        looking towards +z. Points with z near -distance will be clipped.
        """
        pts = np.asarray(points, dtype=float)
        if pts.ndim != 2 or pts.shape[1] != 3:
            raise ValueError("points must be (N,3) array")

        if self.mode == "orthographic":
            return pts[:, :2]

        # perspective: simple pinhole camera
        d = self.distance
        z = pts[:, 2]
        scale = d / (d + z + 1e-9)
        xy = pts[:, :2] * scale[:, None]
        return xy

    def project_rotated(
        self, points: np.ndarray, angles: tuple[float, ...]
    ) -> np.ndarray:
        """Rotate then project points. Angles in degrees."""
        rot = self.rotate(points, angles)
        return self.project(rot)


def animate_cube(proj: Optional[Projection] = None, save: Optional[str] = None) -> None:
    """Demo: animate a rotating cube projected to 2D.

    Args:
        proj: optional Projection instance. If None, uses perspective.
        save: filename to save animation (mp4 or gif) or None to just show.
    """
    if proj is None:
        proj = Projection(mode="perspective", distance=6.0)

    # cube vertices centered at origin
    v = np.array([
        [-1, -1, -1], [+1, -1, -1], [+1, +1, -1], [-1, +1, -1],
        [-1, -1, +1], [+1, -1, +1], [+1, +1, +1], [-1, +1, +1],
    ], dtype=float)

    # cube edges as pairs of vertex indices
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),  # bottom
        (4, 5), (5, 6), (6, 7), (7, 4),  # top
        (0, 4), (1, 5), (2, 6), (3, 7),  # verticals
    ]

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_aspect("equal")
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.axis("off")

    lines = [ax.plot([], [], "k-", lw=2)[0] for _ in edges]

    def init():
        for ln in lines:
            ln.set_data([], [])
        return lines

    def update(frame: int):
        angle = frame / 20.0 * 360.0
        pts2 = proj.project_rotated(v, (angle, angle * 0.6, angle * 0.3))

        for (i, j), ln in zip(edges, lines):
            x = [pts2[i, 0], pts2[j, 0]]
            y = [pts2[i, 1], pts2[j, 1]]
            ln.set_data(x, y)
        return lines

    ani = FuncAnimation(
        fig, update, frames=range(0, 720), init_func=init, interval=30, blit=True
    )

    plt.tight_layout()
    if save:
        ani.save(save, fps=30)
        plt.close(fig)
        print(f"✔ Saved animation to {save}")
    else:
        plt.show()


__all__ = [
    # Base classes
    "BaseAnimator",
    "PhysicsAnimator",
    # Panel system
    "PlotPanel",
    "TRAJECTORY_PANEL",
    "VELOCITY_PANEL",
    "ENERGY_PANEL",
    "STATE_PANEL",
    # Factory
    "animate",
    # Projection utilities
    "Projection",
    "animate_cube",
]