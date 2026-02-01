"""Stress transformation animation export.

Provides export to MP4 and GIF formats.
"""

from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class StressAnimation:
    """
    Export stress transformation animation to video or GIF.

    Creates an animation showing how stress components change
    as the coordinate system rotates through 360 degrees.

    Example:
        >>> from mechlab.visual import StressAnimation
        >>> anim = StressAnimation(100, 50, 25)
        >>> anim.save_gif("stress.gif")
    """

    def __init__(self, sx: float, sy: float, txy: float) -> None:
        """
        Initialize animation exporter.

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
        theta = np.linspace(0, 2*np.pi, 100)
        x_circle = self.center + self.radius * np.cos(theta)
        y_circle = self.radius * np.sin(theta)
        self.ax_circle.plot(x_circle, y_circle, "b-", lw=2)
        self.ax_circle.axhline(y=0, color='k', lw=0.5)
        self.ax_circle.axvline(x=0, color='k', lw=0.5)
        
        # Animation elements
        self.point, = self.ax_circle.plot([], [], "ro", ms=10)
        self.line, = self.ax_path.plot([], [], "b-", lw=2)
        self.path_point, = self.ax_path.plot([], [], "ro", ms=8)
        self.angle_text = self.ax_circle.text(0.02, 0.98, "", transform=self.ax_circle.transAxes,
                                               verticalalignment="top", fontsize=10)
        
        self.sigma_path = []
        self.tau_path = []

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
            frames=np.linspace(0, 2*np.pi, 200),
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
        """
        Save animation as MP4 video.

        Args:
            filename: Output filename
            fps: Frames per second
            frames: Total number of frames
        """
        self._init()
        ani = FuncAnimation(
            self.fig,
            self._update,
            frames=np.linspace(0, 2*np.pi, frames),
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
        """
        Save animation as GIF.

        Args:
            filename: Output filename
            fps: Frames per second
            frames: Total number of frames
        """
        self._init()
        ani = FuncAnimation(
            self.fig,
            self._update,
            frames=np.linspace(0, 2*np.pi, frames),
            init_func=self._init,
            blit=True,
        )
        plt.tight_layout()
        ani.save(filename, fps=fps, writer="pillow")
        print(f"✔ Saved GIF: {filename}")
        plt.close(self.fig)
