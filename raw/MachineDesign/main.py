import numpy as np
def life_measure(L :float, L_10 :float) -> float:
    return L/L_10
def L_D(rL_D :float, n_D :int) -> float:
    return 60*rL_D*n_D

print(life_measure(L_D(30000, 300), 1e+6))

def C_10(a_f :float, F_d : float, x_D :float, x_0 :float, theta :float, R_D :float, a :float, b :float) -> float:
    return a_f * F_d * ((x_D)/(x_0 + (theta - x_0)*np.log(1/R_D)**(1/b)))**(1/a)

print(C_10(1.2, 1837, 540, 0.02, 4.439, 0.99, 3, 1.483))


# realibility vs life ; the weibull distribution
import numpy as np
import matplotlib.pyplot as plt

# --- 1. Parameters ---
x_0 = 0.02     # Guaranteed minimum life
theta = 4.439  # Characteristic life
b = 1.483      # Weibull slope / shape parameter

# --- 2. Data Generation ---
# Generating dimensionless life values from 0 to 10 for a clear view
x = np.linspace(0, 10, 1000)

# Calculate Reliability R(x)
R = np.ones_like(x)
mask = x >= x_0
R[mask] = np.exp(-((x[mask] - x_0) / (theta - x_0))**b)

# Calculate Probability of Failure / Destruction F(x)
F = 1 - R

# --- 3. Plotting Setup ---
plt.figure(figsize=(10, 6))

# Plot the main Reliability and Destruction curves
plt.plot(x, R, label='Reliability $R(x)$', color='blue', linewidth=2.5)
plt.plot(x, F, label='Destruction $F(x)$', color='red', linestyle='--', linewidth=2.5)

# --- 4. Annotating x_0 (The "Immortality Zone") ---
plt.axvline(x=x_0, color='green', linestyle='-', alpha=0.5, label=f'Guaranteed Min Life ($x_0$ = {x_0})')
# Shade the safe zone green
plt.fill_between(x, 0, 1, where=(x <= x_0), color='green', alpha=0.2)
plt.text(x_0 + 0.1, 0.5, 'Safe\nZone', color='green', fontweight='bold')

# --- 5. Annotating theta (The Universal Anchor Point) ---
plt.axvline(x=theta, color='purple', linestyle=':', linewidth=2, label=f'Characteristic Life ($\\theta$ = {theta})')

# Calculate the exact mathematical Y-values at theta (R = 1/e, F = 1 - 1/e)
R_theta = np.exp(-1)
F_theta = 1 - np.exp(-1)

# Draw horizontal guide lines to those intersections
plt.axhline(y=R_theta, color='gray', linestyle=':', alpha=0.7)
plt.axhline(y=F_theta, color='gray', linestyle=':', alpha=0.7)

# Plot the exact dots at the intersections
plt.scatter([theta, theta], [R_theta, F_theta], color='black', zorder=5, s=60)

# Add text labels for the 36.8% and 63.2% points
plt.text(theta + 0.15, R_theta + 0.02, f'R ≈ {R_theta*100:.1f}%', color='blue', fontweight='bold')
plt.text(theta + 0.15, F_theta - 0.04, f'F ≈ {F_theta*100:.1f}%', color='red', fontweight='bold')

# --- 6. Formatting and Display ---
plt.xlabel('Dimensionless Life ($x = L/L_{10}$)', fontsize=12)
plt.ylabel('Probability', fontsize=12)
plt.title(f'Weibull Life Parameters (Shape Parameter $b$ = {b})', fontsize=14, fontweight='bold')
plt.grid(True, linestyle='--', alpha=0.4)
plt.legend(loc='center right', fontsize=10)

plt.xlim(0, 10)
plt.ylim(0, 1.05)
plt.tight_layout()

# Show the plot
plt.show()

