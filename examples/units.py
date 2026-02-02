from mechlab.units import convert

# Convert 100 MPa to psi
psi_value = convert(100, 'MPa', 'psi')
print(f"100 MPa = {psi_value:.2f} psi")

# Convert 1 meter to feet
feet = convert(1, 'm', 'ft')
print(f"1 m = {feet:.4f} ft")

# convert 1L to m3
cubic_meters = convert(1, 'm3', 'L')
print(f"1 m3 = {cubic_meters:.6f} L")

