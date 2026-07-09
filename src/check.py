from mechlab import BeamAnalysis
from mechlab.domain.entities import Material, Section

steel = Material(name="Steel A36", young_modulus=200e9, yield_strength=250e6)
# Replace line 5 with this:
section = Section(
    name="W150x18",
    moment_of_inertia=9.19e-6,
    area=2.3e-3,
    extreme_fiber_distance=0.076
)

F1 = 11120.554  # N, downward positive
F2 = 4448.222   # N, downward positive
M1 = 1500.0     # N-m, CCW positive - applied moment

analysis = BeamAnalysis(length=(203.200 * 3), material=steel, section=section)
analysis.set_simple_supports(pos_a=0, pos_b=analysis.beam.length)
analysis.add_point_load(position=(203.200), magnitude=F1)
analysis.add_point_load(position=(2 * 203.200), magnitude=F2)
analysis.add_moment(position=(1.5 * 203.200), magnitude=M1)   # <-- new: applied couple

report = analysis.run()
print(report)
print(f"Max Bending Stress: {report['max_bending_stress_Pa']:.2f} Pa")
print(f"Max Bending Stress Location: {report['max_bending_stress_location_m']:.2f} m")
print(f"Safety Factor: {report['safety_factor']:.4f}")

try:
    analysis.plot_bending_moment_diagram(show=True, save_path="bending_moment_diagram.png")
    analysis.fbd_beam(show=True, save_path="free_body_diagram.png")
except ImportError:
    print("Skipping plots because matplotlib is not installed. Install with: uv sync --extra plots")
