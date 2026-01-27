# No more messy deep imports!
from mechlab.mechanics import Beam, RigidBody, PrincipalStresses

# Use Statics
my_beam = Beam(L=5, E=200e9, I=1e-4)
print(f"Deflection: {my_beam.max_deflection(1000)}")

# Use Dynamics
particle = RigidBody(mass=10, position=(0,0))
print(f"Weight: {particle.weight()} N")

# Use Stress
tensor = [[100, 30, 0], [30, 50, 0], [0, 0, 0]]
print(f"Principal Stresses: {PrincipalStresses.calculate(tensor)}")