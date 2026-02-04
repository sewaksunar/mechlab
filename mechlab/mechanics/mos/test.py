"""DEFINITION OF STRESS AT A POINT"""
from mechlab.mechanics.mos.stress import Stress, StressTensor, StressArbitraryPlane
from mechlab.mechanics.mos.stress import StressTransfomation
sate = StressArbitraryPlane(1000, 1500, 2000, 10, 15, 20, 300, 400, 500, 5, 6, 7)
sate.stress_tensor()
print("Normal Stress Components (N/m^2):", sate.normal_stress())
print("Shear Stress Components (N/m^2):", sate.shear_stress())
print("Stress Tensor (N/m^2):\n", sate.stress_tensor())
print("Stress on Arbitrary Plane (N/m^2):", sate.traction_stress(1, 1, 1))

print("Stress on oblique plane (N/m^2):", sate.normal_stress())
print("Shear Stress on oblique plane (N/m^2):", sate.shear_stress())

print("Stress transfomation example:")
transform = StressTransfomation(1000, 1500, 2000, 10, 15, 20, 30)
print("Transformed Stress Tensor:", transform.transformed_stress())

# Mohr's circle save example
out_file = 'mohr_xy_example.png'
sate.save_mohr_circle(out_file, plane='xy')
import os
print(f"Mohr plot saved to: {out_file} -> Exists: {os.path.exists(out_file)}")

# The state of stress at a point in a machine part is given by:
# σxx = 10, σyy = 30, σzz = 15, and σxy = σxz = σyz = 0
# Determine the principal stresses and orientation of the principal axes at the point.

print("\nPrincipal Stresses Example:")
# Use σxy = 7.5 to demonstrate oblique-plane principal directions
principal_stress = StressTensor(10, 30, 15, 7.5, 0, 0)
print("Principal Stresses (N/m^2):", principal_stress.principal_stresses())
print("Principal Stress Directions:", principal_stress.principal_directions())

# make mohr's circle
print("\nMohr's Circle Example:")
