"""Stress visualization: interactive viewer and animation export.

Consolidated module providing:
  - StressViewer: Interactive viewer with sliders and Mohr's circle
  - StressAnimation: Export stress transformation to MP4/GIF

Merged from: viewer.py + animation.py
"""

from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button, RadioButtons


class StressViewer:
    """
    Interactive stress transformation viewer with matplotlib.

    Combines stress analysis, Mohr's circle, and animation in one viewer.

    Attributes:
        sx: Normal stress in x-direction
        sy: Normal stress in y-direction
        txy: Shear stress
        unit: Stress unit (default: MPa)

    Example:
        >>> from mechlab.visual import StressViewer
        >>> viewer = StressViewer(100, 50, 25)
        >>> viewer.show()
    """

    def __init__(
        self,
        sx: float = 100,
        sy: float = 50,
        txy: float = 25,
        unit: str = "MPa",
    ) -> None:
        """
        Initialize stress viewer.

        Args:
            sx: Normal stress in x-direction
            sy: Normal stress in y-direction
            txy: Shear stress
            unit: Stress unit
        """
        self.sx = sx
        self.sy = sy
        self.txy = txy
        self.unit = unit
        
        self.theta = 0.0
        self.running = False
        self.sigma_path = []
        self.tau_path = []
        
        self._setup_figure()
        self._setup_sliders()
        self._setup_controls()
        self._update(None)

    def _setup_figure(self) -> None:
        """Create figure with subplots."""
        self.fig = plt.figure(figsize=(12, 5))
        
        # Results text panel
        self.ax_text = self.fig.add_axes([0.02, 0.4, 0.2, 0.5])
        self.ax_text.axis("off")
        self.text = self.ax_text.text(0, 0.9, "", fontfamily="monospace", 
                                       fontsize=10, verticalalignment="top")
        
        # Mohr's circle
        self.ax_mohr = self.fig.add_axes([0.3, 0.35, 0.35, 0.6])
        self.ax_mohr.set_aspect("equal")
        self.ax_mohr.grid(True, alpha=0.3)
        self.ax_mohr.set_xlabel("σ (Normal Stress)")
        self.ax_mohr.set_ylabel("τ (Shear Stress)")
        self.ax_mohr.set_title("Mohr's Circle")
        
        # Stress path
        self.ax_path = self.fig.add_axes([0.72, 0.35, 0.25, 0.6])
        self.ax_path.grid(True, alpha=0.3)
        self.ax_path.set_xlabel("σ")
        self.ax_path.set_ylabel("τ")
        self.ax_path.set_title("Transformation Path")
        
        self.line_path, = self.ax_path.plot([], [], "b-", lw=1.5)
        self.point_path, = self.ax_path.plot([], [], "ro", ms=8)

    def _setup_sliders(self) -> None:
        """Create input sliders."""
        slider_color = "lightblue"
        
        ax_sx = self.fig.add_axes([0.3, 0.22, 0.4, 0.03])
        ax_sy = self.fig.add_axes([0.3, 0.15, 0.4, 0.03])
        ax_txy = self.fig.add_axes([0.3, 0.08, 0.4, 0.03])
        
        self.slider_sx = Slider(ax_sx, "σx", -500, 500, valinit=self.sx, color=slider_color)
        self.slider_sy = Slider(ax_sy, "σy", -500, 500, valinit=self.sy, color=slider_color)
        self.slider_txy = Slider(ax_txy, "τxy", -500, 500, valinit=self.txy, color=slider_color)
        
        for slider in (self.slider_sx, self.slider_sy, self.slider_txy):
            slider.on_changed(self._update)
        
        # Unit selector
        ax_unit = self.fig.add_axes([0.02, 0.08, 0.12, 0.2])
        self.radio_unit = RadioButtons(ax_unit, ("MPa", "GPa", "psi"))
        self.radio_unit.on_clicked(self._on_unit_change)

    def _setup_controls(self) -> None:
        """Create animation controls."""
        ax_theta = self.fig.add_axes([0.78, 0.15, 0.18, 0.03])
        self.slider_theta = Slider(ax_theta, "θ", 0, 360, valinit=0, color="lightgreen")
        self.slider_theta.on_changed(self._on_theta_change)
        
        ax_play = self.fig.add_axes([0.78, 0.08, 0.08, 0.04])
        ax_reset = self.fig.add_axes([0.88, 0.08, 0.08, 0.04])
        
        self.btn_play = Button(ax_play, "▶ Play")
        self.btn_reset = Button(ax_reset, "↺ Reset")
        
        self.btn_play.on_clicked(self._toggle_animation)
        self.btn_reset.on_clicked(self._reset_path)
        
        self.timer = self.fig.canvas.new_timer(interval=50)
        self.timer.add_callback(self._animate)

    def _calculate(self) -> dict:
        """Calculate all stress values."""
        sx, sy, txy = self.sx, self.sy, self.txy
        
        # Center and radius
        center = (sx + sy) / 2
        radius = np.sqrt(((sx - sy) / 2) ** 2 + txy ** 2)
        
        # Principal stresses
        s1 = center + radius
        s2 = center - radius
        
        # Max shear
        tau_max = radius
        
        # Von Mises
        vm = np.sqrt(sx**2 - sx*sy + sy**2 + 3*txy**2)
        
        # Transformed stresses at theta
        theta_rad = np.radians(self.theta)
        sigma_t = center + radius * np.cos(2 * theta_rad)
        tau_t = -radius * np.sin(2 * theta_rad)
        
        return {
            "center": center,
            "radius": radius,
            "s1": s1,
            "s2": s2,
            "tau_max": tau_max,
            "vm": vm,
            "sigma_t": sigma_t,
            "tau_t": tau_t,
        }

    def _update(self, val) -> None:
        """Update all displays."""
        self.sx = self.slider_sx.val
        self.sy = self.slider_sy.val
        self.txy = self.slider_txy.val
        
        calc = self._calculate()
        
        # Update text
        self.text.set_text(
            f"Input ({self.unit}):\n"
            f"  σx  = {self.sx:>8.1f}\n"
            f"  σy  = {self.sy:>8.1f}\n"
            f"  τxy = {self.txy:>8.1f}\n\n"
            f"Principal:\n"
            f"  σ1  = {calc['s1']:>8.1f}\n"
            f"  σ2  = {calc['s2']:>8.1f}\n\n"
            f"Max Shear:\n"
            f"  τmax= {calc['tau_max']:>8.1f}\n\n"
            f"Von Mises:\n"
            f"  σvm = {calc['vm']:>8.1f}"
        )
        
        # Update Mohr's circle
        self.ax_mohr.clear()
        self.ax_mohr.set_aspect("equal")
        self.ax_mohr.grid(True, alpha=0.3)
        self.ax_mohr.set_xlabel(f"σ ({self.unit})")
        self.ax_mohr.set_ylabel(f"τ ({self.unit})")
        self.ax_mohr.set_title("Mohr's Circle")
        
        # Draw circle
        theta_circle = np.linspace(0, 2*np.pi, 100)
        x_circle = calc['center'] + calc['radius'] * np.cos(theta_circle)
        y_circle = calc['radius'] * np.sin(theta_circle)
        self.ax_mohr.plot(x_circle, y_circle, "b-", lw=2)
        
        # Draw points
        self.ax_mohr.plot(calc['center'], 0, "ko", ms=6, label="Center")
        self.ax_mohr.plot(calc['s1'], 0, "g^", ms=10, label=f"σ1={calc['s1']:.1f}")
        self.ax_mohr.plot(calc['s2'], 0, "rv", ms=10, label=f"σ2={calc['s2']:.1f}")
        self.ax_mohr.plot(calc['sigma_t'], calc['tau_t'], "mo", ms=10, label=f"θ={self.theta:.0f}°")
        
        self.ax_mohr.axhline(y=0, color='k', linewidth=0.5)
        self.ax_mohr.axvline(x=0, color='k', linewidth=0.5)
        self.ax_mohr.legend(loc="upper right", fontsize=8)
        
        # Update transformation path
        margin = calc['radius'] * 0.3 + 50
        self.ax_path.set_xlim(calc['center'] - calc['radius'] - margin,
                              calc['center'] + calc['radius'] + margin)
        self.ax_path.set_ylim(-calc['radius'] - margin, calc['radius'] + margin)
        
        self.fig.canvas.draw_idle()

    def _on_unit_change(self, label: str) -> None:
        """Handle unit selection change."""
        self.unit = label
        self._update(None)

    def _on_theta_change(self, val: float) -> None:
        """Handle theta slider change."""
        self.theta = val
        calc = self._calculate()
        
        self.sigma_path.append(calc['sigma_t'])
        self.tau_path.append(calc['tau_t'])
        
        self.line_path.set_data(self.sigma_path, self.tau_path)
        self.point_path.set_data([calc['sigma_t']], [calc['tau_t']])
        
        self._update(None)

    def _toggle_animation(self, event) -> None:
        """Toggle animation playback."""
        self.running = not self.running
        self.btn_play.label.set_text("⏸ Pause" if self.running else "▶ Play")
        
        if self.running:
            self.timer.start()
        else:
            self.timer.stop()

    def _animate(self) -> None:
        """Animation step."""
        self.theta = (self.theta + 2) % 360
        self.slider_theta.set_val(self.theta)

    def _reset_path(self, event) -> None:
        """Reset transformation path."""
        self.sigma_path.clear()
        self.tau_path.clear()
        self.theta = 0
        self.slider_theta.set_val(0)
        self.line_path.set_data([], [])
        self.point_path.set_data([], [])
        self.fig.canvas.draw_idle()

    def show(self) -> None:
        """Display the interactive viewer."""
        plt.show()

    def save(self, filename: str = "stress_viewer.png", dpi: int = 150) -> None:
        """Save current view to file."""
        self.fig.savefig(filename, dpi=dpi, bbox_inches="tight")
        print(f"✔ Saved to {filename}")


# =============================================================================
# STRESS ANIMATION EXPORT (merged from animation.py)
# =============================================================================

class StressAnimation:
    """Export stress transformation animation to video or GIF.

    Creates an animation showing how stress components change
    as the coordinate system rotates through 360 degrees.

    Example:
        >>> from mechlab.visual import StressAnimation
        >>> anim = StressAnimation(100, 50, 25)
        >>> anim.save_gif("stress.gif")
    """

    def __init__(self, sx: float, sy: float, txy: float) -> None:
        """Initialize animation exporter.

        Args:
            sx: Normal stress in x-direction
            sy: Normal stress in y-direction
            txy: Shear stress
        """
        self.sx = sx
        self.sy = sy
        self.txy = txy
        self._setup_figure()

    def _setup_figure(self) -> None:
        """Create animation figure."""
        self.fig, (self.ax_circle, self.ax_path) = plt.subplots(1, 2, figsize=(10, 5))

        # Mohr's circle subplot
        self.ax_circle.set_aspect("equal")
        self.ax_circle.grid(True, alpha=0.3)
        self.ax_circle.set_xlabel("σ (Normal Stress)")
        self.ax_circle.set_ylabel("τ (Shear Stress)")
        self.ax_circle.set_title("Mohr's Circle")

        # Path subplot
        self.ax_path.set_aspect("equal")
        self.ax_path.grid(True, alpha=0.3)
        self.ax_path.set_xlabel("σ")
        self.ax_path.set_ylabel("τ")
        self.ax_path.set_title("Transformation Path")

        # Calculate circle parameters
        self.center = (self.sx + self.sy) / 2
        self.radius = np.sqrt(((self.sx - self.sy) / 2) ** 2 + self.txy ** 2)

        # Set axis limits
        margin = self.radius * 0.5 + 50
        for ax in (self.ax_circle, self.ax_path):
            ax.set_xlim(self.center - self.radius - margin,
                        self.center + self.radius + margin)
            ax.set_ylim(-self.radius - margin, self.radius + margin)

        # Draw static Mohr's circle
        theta = np.linspace(0, 2 * np.pi, 100)
        x_circle = self.center + self.radius * np.cos(theta)
        y_circle = self.radius * np.sin(theta)
        self.ax_circle.plot(x_circle, y_circle, "b-", lw=2)
        self.ax_circle.axhline(y=0, color="k", lw=0.5)
        self.ax_circle.axvline(x=0, color="k", lw=0.5)

        # Animation elements
        (self.point,) = self.ax_circle.plot([], [], "ro", ms=10)
        (self.line,) = self.ax_path.plot([], [], "b-", lw=2)
        (self.path_point,) = self.ax_path.plot([], [], "ro", ms=8)
        self.angle_text = self.ax_circle.text(
            0.02, 0.98, "", transform=self.ax_circle.transAxes,
            verticalalignment="top", fontsize=10
        )

        self.sigma_path: list[float] = []
        self.tau_path: list[float] = []

    def _transform(self, theta: float) -> tuple[float, float]:
        """Calculate transformed stresses at angle theta (radians)."""
        sigma = self.center + self.radius * np.cos(2 * theta)
        tau = -self.radius * np.sin(2 * theta)
        return sigma, tau

    def _init(self):
        """Initialize animation."""
        self.sigma_path.clear()
        self.tau_path.clear()
        self.line.set_data([], [])
        self.point.set_data([], [])
        self.path_point.set_data([], [])
        self.angle_text.set_text("")
        return self.line, self.point, self.path_point, self.angle_text

    def _update(self, frame: float):
        """Update animation frame."""
        sigma, tau = self._transform(frame)

        self.sigma_path.append(sigma)
        self.tau_path.append(tau)

        self.point.set_data([sigma], [tau])
        self.line.set_data(self.sigma_path, self.tau_path)
        self.path_point.set_data([sigma], [tau])
        self.angle_text.set_text(f"θ = {np.degrees(frame):.0f}°")

        return self.line, self.point, self.path_point, self.angle_text

    def preview(self) -> None:
        """Preview animation in matplotlib window."""
        self.ani = FuncAnimation(
            self.fig,
            self._update,
            frames=np.linspace(0, 2 * np.pi, 200),
            init_func=self._init,
            interval=40,
            blit=True,
        )
        plt.tight_layout()
        plt.show()

    def save_mp4(
        self,
        filename: str = "stress_animation.mp4",
        fps: int = 30,
        frames: int = 200,
    ) -> None:
        """Save animation as MP4 video.

        Args:
            filename: Output filename
            fps: Frames per second
            frames: Total number of frames
        """
        self._init()
        ani = FuncAnimation(
            self.fig,
            self._update,
            frames=np.linspace(0, 2 * np.pi, frames),
            init_func=self._init,
            blit=True,
        )
        plt.tight_layout()
        ani.save(filename, fps=fps, writer="ffmpeg")
        print(f"✔ Saved MP4: {filename}")
        plt.close(self.fig)

    def save_gif(
        self,
        filename: str = "stress_animation.gif",
        fps: int = 20,
        frames: int = 100,
    ) -> None:
        """Save animation as GIF.

        Args:
            filename: Output filename
            fps: Frames per second
            frames: Total number of frames
        """
        self._init()
        ani = FuncAnimation(
            self.fig,
            self._update,
            frames=np.linspace(0, 2 * np.pi, frames),
            init_func=self._init,
            blit=True,
        )
        plt.tight_layout()
        ani.save(filename, fps=fps, writer="pillow")
        print(f"✔ Saved GIF: {filename}")
        plt.close(self.fig)


__all__ = ["StressViewer", "StressAnimation"]