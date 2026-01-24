from mechlab.mechanics.statics.stress import StressOnArbitaryPlane
stress_tensor = [
            [100, 30, 20],
            [30, 80, 10],
            [20, 10, 60]
        ]
normal_vector = [1, 0, 0]
stress_on_plane = StressOnArbitaryPlane.calculate_stress(stress_tensor, normal_vector)
print(stress_on_plane)  # Output: [100, 30, 20], sigma_xx = 100, 

# let stress_tensor be a 3x3 matrix representing the stress tensor in x, y, z rectangular coordinates
# in XYz coordinate system let deirection cosines be defined as follows
'''
    x   y   z
X   l1 m1 n1
Y   l2 m2 n2
Z   l3 m3 n33

    where l1, m1, n1 are direction cosines of X axis with respect to x, y, z axes respectively
    i.e. l1 = cos(angle between X and x axes)
    similarly for other direction cosines
'''
import sympy as sp

# Direction cosines
l1, m1, n1 = sp.symbols('l1 m1 n1')
l2, m2, n2 = sp.symbols('l2 m2 n2')
l3, m3, n3 = sp.symbols('l3 m3 n3')

# Stress tensor components in original x-y-z system
sxx, syy, szz = sp.symbols('sxx syy szz')
sxy, syz, sxz = sp.symbols('sxy syz sxz')

# Direction cosine matrix (rows = new axes X, Y, Z; columns = x, y, z)
direction_cosines = sp.Matrix([
    [l1, m1, n1],
    [l2, m2, n2],
    [l3, m3, n3]
])

# Stress tensor in original coordinates
stress_tensor_xyz = sp.Matrix([
    [sxx, sxy, sxz],
    [sxy, syy, syz],
    [sxz, syz, szz]
])

# Transform: σ' = L * σ * L.T
stress_tensor_XYZ = direction_cosines * stress_tensor_xyz * direction_cosines.T

# Extract transformed components
sXX = stress_tensor_XYZ[0, 0]
sYY = stress_tensor_XYZ[1, 1]
sZZ = stress_tensor_XYZ[2, 2]

print("sXX =", sp.simplify(sXX))
print("sYY =", sp.simplify(sYY))
print("sZZ =", sp.simplify(sZZ))
