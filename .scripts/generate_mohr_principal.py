from mechlab.mechanics.mos.stress import StressTensor
import numpy as np

# Given stress components (MPa) per your problem statement
s = StressTensor(120, 55, -85, -55, -75, 33)
# Save principal Mohr circles plot
out = 'mohr_principal_example.png'
s.plot_principal_mohr(show=False, filename=out)
import os
print(f'Principal Mohr plot saved to: {out} -> Exists: {os.path.exists(out)}')
# Print basic computed results
prin = s.principal_stresses()
print('Principal stresses:', np.round(prin,6))

n1 = np.array([1/np.sqrt(3),1/np.sqrt(3),1/np.sqrt(3)])
Sigma = np.diag(prin)
T1 = Sigma @ n1
sigma_n1 = float(n1 @ T1)
tau1 = float(np.linalg.norm(T1 - sigma_n1*n1))
print('\nN1:', np.round(n1,6))
print('  σ_n =', round(sigma_n1,6), 'MPa')
print('  τ   =', round(tau1,6), 'MPa')
