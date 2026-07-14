import numpy as np
import matplotlib.pyplot as plt
from scipy.special import gamma

# 1. Input Weibull Parameters [Source 3, 476]
x0 = 0.020    # Guaranteed minimum life
theta = 4.459 # Characteristic parameter
b = 1.483     # Shape parameter (skewness)

# Mean Dimensionless Life (mu_x)
mean_x = x0 + (theta - x0) * gamma(1 + 1/b)

# Median Dimensionless Life (x_0.50)
median_x = x0 + (theta - x0) * (np.log(1/0.50))**(1/b)

# 10th Percentile Life (x_0.10) - Corresponds to R=0.90
L10_x = x0 + (theta - x0) * (np.log(1/0.90))**(1/b)

# Standard Deviation (sigma_hat_x)
std_dev_x = (theta - x0) * np.sqrt(gamma(1 + 2/b) - (gamma(1 + 1/b))**2)

# Coefficient of Variation (Cx)
cov_x = std_dev_x / mean_x

# Print Results
print(f"Mean Life: {mean_x:.3f} L10")
print(f"Median Life: {median_x:.3f} L10")
print(f"10th Percentile (L10): {L10_x:.3f}")
print(f"Standard Deviation: {std_dev_x:.3f}")
print(f"Coefficient of Variation: {cov_x:.3f}")

# 3. Visualization [Source 2, 189-204]
x_vals = np.linspace(0, 12, 1000)

# Reliability Function R(x) [Source 3, 474]
reliability = np.exp(-((x_vals - x0) / (theta - x0))**b)
reliability[x_vals < x0] = 1.0 # Reliability is 1.0 before x0

# Probability Density Function f(x) [Source 3, 476]
pdf = np.zeros_like(x_vals)
mask = x_vals >= x0
pdf[mask] = (b / (theta - x0)) * ((x_vals[mask] - x0) / (theta - x0))**(b - 1) * \
            np.exp(-((x_vals[mask] - x0) / (theta - x0))**b)

# Plotting
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Plot PDF
ax1.plot(x_vals, pdf, color='blue', lw=2, label='Weibull PDF')
ax1.fill_between(x_vals, pdf, alpha=0.1, color='blue')

ax1.axvline(L10_x, color='green', linestyle='--', label=f'L10 ({L10_x:.1f})')
ax1.axvline(median_x, color='orange', linestyle='--', label=f'Median ({median_x:.2f})')
ax1.axvline(mean_x, color='red', linestyle='--', label=f'Mean ({mean_x:.2f})')

ax1.set_title('Probability Density Function (Failure Distribution)')
ax1.set_xlabel('Dimensionless Life (x = L/L10)')
ax1.set_ylabel('f(x)')
ax1.legend()
ax1.grid(True)

# Plot Reliability
ax2.plot(x_vals, reliability, color='purple', lw=2, label='Reliability R(x)')
ax2.axhline(0.90, color='gray', linestyle=':', label='R = 0.90')
ax2.axvline(1.0, color='green', linestyle='--', label='L10 Life')
ax2.set_title('Reliability Function (Survival Probability)')
ax2.set_xlabel('Dimensionless Life (x = L/L10)')
ax2.set_ylabel('Reliability R')
ax2.legend()
ax2.grid(True)

plt.tight_layout()
plt.show()

# check 1
# check 2