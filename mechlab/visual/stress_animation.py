# mechlab/visual/stress_animation.py
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class StressRotationAnimation:
    def __init__(self, sx, sy, txy):
        self.sx = sx
        self.sy = sy
        self.txy = txy

        self.theta_vals = []
        self.sigma_vals = []
        self.tau_vals = []

        self.fig, self.ax = plt.subplots()
        self.line, = self.ax.plot([], [], lw=2)

        self.ax.set_xlim(-400, 400)
        self.ax.set_ylim(-400, 400)
        self.ax.set_aspect("equal")
        self.ax.grid(True)
        self.ax.set_title("Stress Transformation Path")

    def _stress_transform(self, theta):
        s_avg = (self.sx + self.sy) / 2
        R = np.sqrt(((self.sx - self.sy) / 2) ** 2 + self.txy ** 2)

        sigma = s_avg + R * np.cos(2 * theta)
        tau = -R * np.sin(2 * theta)
        return sigma, tau

    def _update(self, frame):
        sigma, tau = self._stress_transform(frame)

        self.sigma_vals.append(sigma)
        self.tau_vals.append(tau)

        self.line.set_data(self.sigma_vals, self.tau_vals)
        return (self.line,)

    def animate(self):
        self.ani = FuncAnimation(
            self.fig,
            self._update,
            frames=np.linspace(0, 2 * np.pi, 200),
            interval=40,
            blit=True
        )
        plt.show()

    def save(self, filename="stress_rotation.mp4"):
        self.ani = FuncAnimation(
            self.fig,
            self._update,
            frames=np.linspace(0, 2 * np.pi, 200),
            interval=40,
            blit=True
        )
        self.ani.save(filename, fps=30)
