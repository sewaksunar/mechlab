import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
from matplotlib.animation import FuncAnimation

# --- Configuration ---
r, L = 1.0, 2.5
# State tracks which part is being dragged
state = {'theta': 0.0, 'drag_mode': None, 'animating': False}

# --- Setup Plot ---
fig, ax = plt.subplots(figsize=(6, 8))
ax.set_xlim(-2.5, 2.5)
ax.set_ylim(-1.5, 4.5)
ax.set_aspect('equal')
ax.set_title("DRIVE: Drag Blue Pin (Crank) or Black Box (Piston)\nPress 'A' for Auto-Motor")

# --- Visual Supports ---
# Cylinder Walls
ax.plot([-0.5, -0.5], [1.0, 4.5], color='black', lw=2, alpha=0.3)
ax.plot([0.5, 0.5], [1.0, 4.5], color='black', lw=2, alpha=0.3)
# Crank Path
ax.add_artist(Circle((0, 0), r, color='gray', fill=False, linestyle=':'))

# --- Mechanism Elements ---
crank_line, = ax.plot([], [], 'o-', lw=8, color='dodgerblue', markersize=12, zorder=3)
rod_line, = ax.plot([], [], 'o-', lw=5, color='crimson', zorder=2)
piston_patch = Rectangle((-0.4, 0), 0.8, 0.6, color='black', alpha=0.8, zorder=4)
ax.add_patch(piston_patch)

def update_mechanism(angle):
    cx, cy = r * np.cos(angle), r * np.sin(angle)
    # Solve for piston height py: L^2 = cx^2 + (py - cy)^2
    py = cy + np.sqrt(L**2 - cx**2)
    
    crank_line.set_data([0, cx], [0, cy])
    rod_line.set_data([cx, 0], [cy, py])
    piston_patch.set_xy((-0.4, py))
    return crank_line, rod_line, piston_patch

# --- Interaction Logic ---
def on_click(event):
    if event.inaxes != ax: return
    
    # Calculate current positions
    cx, cy = r * np.cos(state['theta']), r * np.sin(state['theta'])
    py = cy + np.sqrt(L**2 - cx**2)
    
    # 1. Check if clicking Crank Pin
    if np.hypot(event.xdata - cx, event.ydata - cy) < 0.3:
        state['drag_mode'] = 'CRANK'
        state['animating'] = False
    
    # 2. Check if clicking Piston (the black rectangle)
    elif -0.4 <= event.xdata <= 0.4 and py <= event.ydata <= py + 0.6:
        state['drag_mode'] = 'PISTON'
        state['animating'] = False

def on_motion(event):
    if event.inaxes != ax or not state['drag_mode']: return
    
    if state['drag_mode'] == 'CRANK':
        # Driving by rotation
        state['theta'] = np.arctan2(event.ydata, event.xdata)
        
    elif state['drag_mode'] == 'PISTON':
        # Driving by vertical displacement
        # We constrain py to stay within physical limits [L-r, L+r]
        target_py = np.clip(event.ydata, L - r + 0.01, L + r - 0.01)
        
        # Solving for theta: target_py = r*sin(th) + sqrt(L^2 - r^2*cos^2(th))
        # This is non-trivial to invert perfectly, so we use the geometric angle
        # between the rod and the vertical to find the equivalent theta
        cos_beta = (target_py**2 + r**2 - L**2) / (2 * target_py * r)
        cos_beta = np.clip(cos_beta, -1, 1)
        
        # Maintain the 'side' of the crank to prevent jumping
        current_side = np.sign(np.cos(state['theta']))
        state['theta'] = current_side * np.arccos(cos_beta) + np.pi/2

    update_mechanism(state['theta'])
    fig.canvas.draw_idle()

def on_release(event):
    state['drag_mode'] = None

def on_key(event):
    if event.key.lower() == 'a':
        state['animating'] = not state['animating']

def animate(i):
    if state['animating'] and not state['drag_mode']:
        state['theta'] += 0.08
        return update_mechanism(state['theta'])
    return crank_line, rod_line, piston_patch

# Register Callbacks
fig.canvas.mpl_connect('button_press_event', on_click)
fig.canvas.mpl_connect('button_release_event', on_release)
fig.canvas.mpl_connect('motion_notify_event', on_motion)
fig.canvas.mpl_connect('key_press_event', on_key)

ani = FuncAnimation(fig, animate, interval=20, blit=True)
plt.show()