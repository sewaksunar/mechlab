class State:
    """
    Represents a thermodynamic state of a pure substance.

    Usage:
        >>> from mechlab.thermodynamics import State
        >>> water = State("water", T=373.15, P=101325)
        >>> print(f"Enthalpy: {water.h:.2f} J/kg")

    Expected Output:
        .. code-block:: text

           Enthalpy: 2675529.15 J/kg

    The state is defined by two independent intensive properties. 
    Internal logic handles phase detection (Subcooled, Saturated, Superheated).
    """