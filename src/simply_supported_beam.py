"""
Example: 4m steel beam, simply supported at both ends, with a
point load in the middle and a distributed load over part of the span.

Run with:
    PYTHONPATH=src python3 examples/simply_supported_beam.py
"""

from mechlab import BeamAnalysis
from mechlab.domain.entities import Material, Section

steel = Material(name="Steel A36", young_modulus=200e9, yield_strength=250e6)
i_beam = Section(name="W150x18", moment_of_inertia=9.19e-6, area=2.3e-3,
                  extreme_fiber_distance=0.076)

analysis = (
    BeamAnalysis(length=4.0, material=steel, section=i_beam)
    .set_simple_supports(pos_a=0.0, pos_b=4.0)
    .add_point_load(position=2.0, magnitude=5000)       # 5 kN at midspan
    .add_distributed_load(start=0.0, end=4.0, intensity=1000)  # 1 kN/m UDL
)

report = analysis.run()

print("Reactions (position m, force N):")
for pos, force in report["reactions"]:
    print(f"  x={pos}m -> R={force:.2f} N")

print(f"\nMax bending stress: {report['max_bending_stress_Pa']/1e6:.2f} MPa "
      f"at x={report['max_bending_stress_location_m']:.2f} m")
print(f"Safety factor vs yield: {report['safety_factor']:.2f}")
