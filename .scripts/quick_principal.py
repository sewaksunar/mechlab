from mechlab.mechanics.mos.stress import StressTensor
import numpy as np
s = StressTensor(10, 30, 15, 13.333333333, 0, 0)
print('stress tensor:\n', s.stress_tensor())
print('principal stresses:', np.round(s.principal_stresses(), 6))
pd = s.principal_directions()
print('principal directions (columns):')
print(pd)
print('\nRounded:')
print(np.round(pd, 4))