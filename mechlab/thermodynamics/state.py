import numpy as np
import sympy as sp

# Symbols for SymPy equations
P, V, n, R, T = sp.symbols('P V n R T')

def enthalpy_TP(fluid: str, temp: float, press: float) -> float:
    """Calculates Enthalpy (Simplified Ideal Gas Model: H = Cp * T)"""
    cp_air = 1005  # J/kg-K
    return float(cp_air * temp)

def entropy_TP(fluid: str, temp: float, press: float) -> float:
    """Calculates Entropy (Simplified Model)"""
    return float(1.0 * temp / press)

def get_pressure_func():
    """Returns a numerical function for P = nRT/V"""
    ideal_gas_eq = (n * R * T) / V
    return sp.lambdify((n, R, T, V), ideal_gas_eq, 'numpy')