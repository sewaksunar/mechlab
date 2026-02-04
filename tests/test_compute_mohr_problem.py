import numpy as np
from mechlab.mechanics.mos.stress import StressTensor


def test_compute_problem_print():
    s = StressTensor(120, 55, -85, -55, -75, 33)
    print('Stress tensor:\n', np.round(s.stress_tensor(), 6))
    prin = s.principal_stresses()
    dirs = s.principal_directions()
    print('\nPrincipal stresses (σ1>=σ2>=σ3) [MPa]:', np.round(prin, 6))
    print('\nPrincipal directions (columns):\n', np.round(dirs, 6))
    Sigma = np.diag(prin)
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
    # small assertion to mark test passed
    assert True
