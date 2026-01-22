from CoolProp.CoolProp import PropsSI

def enthalpy_TP(fluid: str, T: float, P: float) -> float:
    """
    Enthalpy [J/kg]
    T in Kelvin, P in Pascal
    """
    return PropsSI("H", "T", T, "P", P, fluid)

def entropy_TP(fluid: str, T: float, P: float) -> float:
    """
    Entropy [J/kg-K]
    """
    return PropsSI("S", "T", T, "P", P, fluid)
