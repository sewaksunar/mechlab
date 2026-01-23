from mechlab.mechanics import Beam
# Define a beam: Length=2m, E=210GPa, I=1e-5 m^4
my_beam = Beam(L=3.0, E=210e9, I=1e-5)
print(f"Max Deflection: {my_beam.max_deflection(load=5000):.5f} m")