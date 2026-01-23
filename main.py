from mechlab.thermodynamics import state

# Define system parameters
moles = 1.0       # n
gas_const = 8.314 # R (J/mol·K)
temp = 300        # T (Kelvin)
volume = 0.025    # V (m^3)

# Get the pressure function
p_func = state.get_pressure_func()
pressure = p_func(moles, gas_const, temp, volume)

print(f"The system pressure is: {pressure:.2f} Pa")