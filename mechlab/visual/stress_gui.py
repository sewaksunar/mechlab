"""Interactive GUI for stress visualization."""

import math
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider


class StressGUI:
    """Interactive principal stress viewer with sliders."""
    def __init__(self, sx, sy, txy):
        self.sx, self.sy, self.txy = sx, sy, txy

        self.fig, self.ax = plt.subplots()
        plt.subplots_adjust(bottom=0.35)

        self.ax.set_title("Principal Stress Viewer")
        self.ax.set_xlim(-1, 1)
        self.ax.set_ylabel("Stress")

        self._add_sliders()
        self.update(None)

        plt.show()

    def principal(self):
        avg = (self.sx + self.sy) / 2
        r = math.sqrt(((self.sx - self.sy)/2)**2 + self.txy**2)
        return avg + r, avg - r

    def _add_sliders(self):
        ax_sx = plt.axes([0.2, 0.25, 0.6, 0.03])
        ax_sy = plt.axes([0.2, 0.20, 0.6, 0.03])
        ax_t  = plt.axes([0.2, 0.15, 0.6, 0.03])

        self.sx_slider = Slider(ax_sx, 'σx', -500, 500, valinit=self.sx)
        self.sy_slider = Slider(ax_sy, 'σy', -500, 500, valinit=self.sy)
        self.t_slider  = Slider(ax_t,  'τxy', -500, 500, valinit=self.txy)

        for s in (self.sx_slider, self.sy_slider, self.t_slider):
            s.on_changed(self.update)

    def update(self, val):
        self.sx = self.sx_slider.val
        self.sy = self.sy_slider.val
        self.txy = self.t_slider.val

        s1, s2 = self.principal()

        self.ax.clear()
        self.ax.scatter([0, 0], [s1, s2])
        self.ax.set_title("Principal Stresses")
        self.ax.set_xlim(-1, 1)
        self.ax.set_ylim(-600, 600)
        self.ax.set_ylabel("Stress")

        self.fig.canvas.draw_idle()
