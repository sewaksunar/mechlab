"""Stress animation export utilities."""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class StressAnimationExporter:
    """Export stress transformation animations to MP4 or GIF."""
    def __init__(self, sx, sy, txy):
        self.sx = sx
        self.sy = sy
        self.txy = txy

        self.fig, self.ax = plt.subplots()
        self.line, = self.ax.plot([], [], lw=2)

        self.sigma_vals = []
        self.tau_vals = []

        self.ax.set_xlim(-400, 400)
        self.ax.set_ylim(-400, 400)
        self.ax.set_aspect("equal")
        self.ax.grid(True)
        self.ax.set_title("Stress Transformation")

    def _stress_transform(self, theta):
        s_avg = (self.sx + self.sy) / 2
        R = np.sqrt(((self.sx - self.sy) / 2) ** 2 + self.txy ** 2)

        sigma = s_avg + R * np.cos(2 * theta)
        tau = -R * np.sin(2 * theta)
        return sigma, tau

    def _update(self, theta):
        sigma, tau = self._stress_transform(theta)

        self.sigma_vals.append(sigma)
        self.tau_vals.append(tau)

        self.line.set_data(self.sigma_vals, self.tau_vals)
        return (self.line,)

    def export_mp4(self, filename="stress.mp4", frames=200, fps=30):
        ani = FuncAnimation(
            self.fig,
            self._update,
            frames=np.linspace(0, 2 * np.pi, frames),
            blit=True
        )

        ani.save(filename, fps=fps)
        print(f"✔ Exported MP4 → {filename}")

    def export_gif(self, filename="stress.gif", frames=200, fps=20):
        ani = FuncAnimation(
            self.fig,
            self._update,
            frames=np.linspace(0, 2 * np.pi, frames),
            blit=True
        )

        ani.save(filename, writer="pillow", fps=fps)
        print(f"✔ Exported GIF → {filename}")
