from sympy.vector import CoordSys3D
N = CoordSys3D('N')
Fx = 2 * N.i
Fy = 3 * N.j
Fz = 4 * N.k
F = 3 * N.i + 4 * N.j + 5 * N.k
magnitude_F = F.magnitude()
print("Magnitude of F:", magnitude_F)
dot_product = F.dot(N.i)