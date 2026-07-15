import sympy as sp

# 1. Define the symbolic variable
theta = sp.Symbol('theta', real=True)

# 2. Define the equation
equation = sp.sin(theta)**2 - 6*sp.cos(theta) - 3

# 3. Solve the equation analytically
solutions = sp.solve(equation, theta)

print("Solutions for theta in [0, 2*pi):")

for sol in solutions:
    # CRITICAL FIX: Only process real numbers, skip complex imaginary roots
    if not sol.is_real:
        continue
        
    # Handle negative angle representations by wrapping them into [0, 2*pi)
    if sol.evalf() < 0:
        sol = sol + 2*sp.pi
        
    # Calculate numeric values
    rad_val = float(sol.evalf())
    deg_val = float(sp.deg(sol).evalf())
    
    print(f"\n  Symbolic: theta = {sol}")
    print(f"  Radians:  {rad_val:.4f} rad")
    print(f"  Degrees:  {deg_val:.2f}°")
