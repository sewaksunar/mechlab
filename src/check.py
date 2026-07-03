from mechlab import BeamAnalysis
from mechlab.domain.entities import Material, Section

steel = Material(name="Steel A36", young_modulus=200e9, yield_strength=250e6)
section = Section(name="W150x18", moment_of_inertia=9.19e-6, area=2.3e-3,
                   extreme_fiber_distance=0.076)

# analysis = (
#     BeamAnalysis(length=(400+350+300), material=steel, section=section)
#     .set_simple_supports(pos_a=0.0, pos_b=4.0)
#     .add_point_load(position=2.0, magnitude=5000)
#     .add_distributed_load(start=0.10, end=2.0, intensity=1000)
# )
F1 = 11120.554  # N, downward positive
F2 = 4448.222   # N, downward positive
analysis = BeamAnalysis(length=(203.200*3), material=steel, section=section)
analysis.set_simple_supports(pos_a=0, pos_b=analysis.beam.length)
analysis.add_point_load(position=(203.200), magnitude=F1)
analysis.add_point_load(position=(2*203.200), magnitude=F2)
# analysis.set_support(position=175, support_type=SupportType.PIN)

report = analysis.run()
print(report)
# Assuming 'report' is the variable holding the dictionary
print(f"Max Bending Stress: {report['max_bending_stress_Pa']:.2f} Pa")
print(f"Max Bending Stress Location: {report['max_bending_stress_location_m']:.2f} m")
print(f"Safety Factor: {report['safety_factor']:.4f}")

analysis.plot_bending_moment_diagram(show=True, save_path="bending_moment_diagram.png")
analysis.fbd_beam(show=True, save_path="free_body_diagram.png")
