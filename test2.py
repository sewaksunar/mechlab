import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np

def mohrs_circle(sigma_x, sigma_y, tau_xy):
    center = (sigma_x + sigma_y)/2
    radius = np.sqrt(((sigma_x - sigma_y)/2)**2 + tau_xy**2)
    theta = np.linspace(0, 2*np.pi, 200)
    return center + radius*np.cos(theta), radius*np.sin(theta)

# Initial values
sigma_x, sigma_y, tau_xy = 50, 30, 20
circle_x, circle_y = mohrs_circle(sigma_x, sigma_y, tau_xy)

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.25)
line, = ax.plot(circle_x, circle_y, 'b-')
ax.set_title("Mohr's Circle (Interactive)")

# Slider for tau_xy
ax_tau = plt.axes([0.25, 0.1, 0.65, 0.03])
slider_tau = Slider(ax_tau, 'τxy', -100, 100, valinit=tau_xy)

def update(val):
    tau = slider_tau.val
    cx, cy = mohrs_circle(sigma_x, sigma_y, tau)
    line.set_xdata(cx)
    line.set_ydata(cy)
    fig.canvas.draw_idle()

slider_tau.on_changed(update)
plt.show()
