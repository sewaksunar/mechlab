import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

class StressInteractive:
    def __init__(self, sx, sy, txy):
        self.sx = sx
        self.sy = sy
        self.txy = txy

        self.theta = 0.0
        self.running = False

        self.fig, self.ax = plt.subplots()
        plt.subplots_adjust(bottom=0.3)

        self.line, = self.ax.plot([], [], lw=2)
        self.point, = self.ax.plot([], [], 'ro')

        self.sigma_vals = []
        self.tau_vals = []

        self.ax.set_xlim(-400, 400)
        self.ax.set_ylim(-400, 400)
        self.ax.set_aspect("equal")
        self.ax.grid(True)
        self.ax.set_title("Stress Transformation (Interactive)")

        self._add_slider()
        self._add_button()

        self.timer = self.fig.canvas.new_timer(interval=50)
        self.timer.add_callback(self._auto_update)

    def _stress_transform(self, theta):
        s_avg = (self.sx + self.sy) / 2
        R = np.sqrt(((self.sx - self.sy) / 2) ** 2 + self.txy ** 2)

        sigma = s_avg + R * np.cos(2 * theta)
        tau = -R * np.sin(2 * theta)
        return sigma, tau

    def _add_slider(self):
        ax_theta = plt.axes([0.2, 0.15, 0.6, 0.03])
        self.theta_slider = Slider(
            ax_theta, "θ (rad)", 0, 2 * np.pi, valinit=0
        )
        self.theta_slider.on_changed(self._slider_update)

    def _add_button(self):
        ax_btn = plt.axes([0.45, 0.05, 0.1, 0.05])
        self.btn = Button(ax_btn, "Play")
        self.btn.on_clicked(self._toggle)

    def _slider_update(self, val):
        self.theta = val
        self._update_plot(reset=True)

    def _toggle(self, event):
        self.running = not self.running
        self.btn.label.set_text("Pause" if self.running else "Play")

        if self.running:
            self.timer.start()
        else:
            self.timer.stop()

    def _auto_update(self):
        self.theta += 0.05
        if self.theta > 2 * np.pi:
            self.theta = 0
            self.sigma_vals.clear()
            self.tau_vals.clear()

        self.theta_slider.set_val(self.theta)

    def _update_plot(self, reset=False):
        sigma, tau = self._stress_transform(self.theta)

        if reset:
            self.sigma_vals.clear()
            self.tau_vals.clear()

        self.sigma_vals.append(sigma)
        self.tau_vals.append(tau)

        self.line.set_data(self.sigma_vals, self.tau_vals)
        self.point.set_data([sigma], [tau])

        self.fig.canvas.draw_idle()

    def show(self):
        plt.show()
