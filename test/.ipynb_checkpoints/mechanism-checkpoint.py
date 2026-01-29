import sympy as sp
from mechlab.mechanics.stress import StressState

# Numeric test
state = StressState(100, 50, 25)
print("Principal stresses:", state.principal_stresses())
print("Max shear:", state.max_shear())

# Symbolic test
sx, sy, t = sp.symbols("σx σy τxy")
sym_state = StressState(sx, sy, t)
sym_state.pretty()
