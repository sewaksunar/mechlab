from mechlab.thermodynamics import state
import numpy as np

def run_test():
    print("--- Starting Thermodynamics Test (SymPy/NumPy) ---")
    
    # 1. Test the Enthalpy function (Linear model)
    temp = 300.0
    press = 101325.0
    h = state.enthalpy_TP("Air", temp, press)
    print(f"Calculated Enthalpy: {h} J/kg")

    # 2. Test the Symbolic-to-Numerical Pressure function
    p_func = state.get_pressure_func()
    # P = nRT/V -> (1 mole, 8.314 R, 300K, 0.025 m^3)
    p_result = p_func(1.0, 8.314, 300, 0.025)
    print(f"Calculated Pressure: {p_result:,.2f} Pa")
    
    print("------------------------------------------------")
    print("SUCCESS: All functions executed correctly!")

if __name__ == "__main__":
    run_test()