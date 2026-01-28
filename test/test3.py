# No more messy deep imports!
from mechlab.mechanics import Beam, RigidBody, PrincipalStresses
from mechlab.mechanics.statics import StaticsParticle

# Use Statics
my_beam = Beam(L=5, E=200e9, I=1e-4)
print(f"Deflection: {my_beam.max_deflection(1000)}")

# Use Dynamics
particle = RigidBody(mass=10, position=(0,0))
print(f"Weight: {particle.weight()} N")

# Use Stress
tensor = [[100, 30, 0], [30, 50, 0], [0, 0, 0]]
print(f"Principal Stresses: {PrincipalStresses.calculate(tensor)}")

# Use StaticsParticle
statics_particle = StaticsParticle(forces=[[10, 20, -5], [-5, 15, 10]])
print(f"Resultant Force: {statics_particle.resultant()} N")
print(f"Inclination Angles (radians): {statics_particle.inclination()}")
print(f"Resolved Components: {statics_particle.resolve_components()} N")
print(f"Unit Vector: {statics_particle.unit_vector()}")