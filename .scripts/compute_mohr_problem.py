from mechlab.mechanics.mos.stress import StressTensor
import numpy as np

# Given stress components (MPa) in the problem statement
# Interpreted as: sigma_xx=120, sigma_yy=55, sigma_zz=-85
#                   tau_xy=-55, tau_yz=-75, tau_zx=33
s = StressTensor(120, 55, -85, -55, -75, 33)
print('Stress tensor (global):\n', np.round(s.stress_tensor(), 6))

# Compute principal stresses and directions
prin = s.principal_stresses()
dirs = s.principal_directions()
print('\nPrincipal stresses (σ1>=σ2>=σ3) [MPa]:', np.round(prin, 6))
print('\nPrincipal directions (columns):\n', np.round(dirs, 6))

# Principal stress matrix (diagonal)
Sigma = np.diag(prin)

# Normals relative to principal axes
n1 = np.array([1/np.sqrt(3), 1/np.sqrt(3), 1/np.sqrt(3)])
n2 = np.array([1/np.sqrt(2), 1/np.sqrt(2), 0.0])

for idx, n in enumerate([n1, n2], start=1):
    T = Sigma @ n
    sigma_n = float(n @ T)
    tau_vec = T - sigma_n * n
    tau = float(np.linalg.norm(tau_vec))
    print(f'\nNormal N{idx} =', np.round(n, 6))
    print(f'  Traction vector T =', np.round(T, 6), 'MPa')
    print(f'  Normal stress σ_n = {sigma_n:.6f} MPa')
    print(f'  Shear vector (components) =', np.round(tau_vec, 6), 'MPa')
    print(f'  Shear magnitude τ = {tau:.6f} MPa')

# Mohr circles for principal pairs
pairs = [(0, 1), (1, 2), (2, 0)]
print('\nMohr circle parameters (principal pairs):')
for a, b in pairs:
    center = 0.5 * (prin[a] + prin[b])
    radius = abs(prin[a] - prin[b]) / 2.0
    print(f'  Circle σ{a+1}-σ{b+1}: center = {center:.6f} MPa, radius = {radius:.6f} MPa, sigmas = ({prin[a]:.6f}, {prin[b]:.6f})')

# Check which circle the (σ_n, τ) point lies on (within tolerance)
for i, n in enumerate([n1, n2], start=1):
    T = Sigma @ n
    sigma_n = float(n @ T)
    tau = float(np.linalg.norm(T - sigma_n * n))
    print(f'\nPoint for N{i}: (σ = {sigma_n:.6f}, τ = {tau:.6f})')
    for a, b in pairs:
        center = 0.5 * (prin[a] + prin[b])
        radius = abs(prin[a] - prin[b]) / 2.0
        dist = np.hypot(sigma_n - center, tau)
        print(f'  distance to circle σ{a+1}-σ{b+1}: {dist:.6f} (radius {radius:.6f})')
    
    # Determine closest circle
    dists = [np.hypot(sigma_n - 0.5 * (prin[a] + prin[b]), tau) for a, b in pairs]
    idx_min = int(np.argmin(np.abs(np.array(dists) - np.array([abs(prin[a]-prin[b])/2.0 for a,b in pairs]))))
    a,b = pairs[idx_min]
    print(f'  Closest circle: σ{a+1}-σ{b+1}')

print('\nDone')