"""Unit conversion utilities for stress and other engineering quantities."""

STRESS_UNITS = {
    "Pa": 1.0,
    "kPa": 1e3,
    "MPa": 1e6,
    "GPa": 1e9,
    "psi": 6894.76,
}


def to_base(value, unit):
    """
    Convert stress value to base unit (Pascals).
    
    Args:
        value: Stress value in specified unit
        unit: Unit name (Pa, kPa, MPa, GPa, psi)
        
    Returns:
        Stress value in Pascals
    """
    return value * STRESS_UNITS[unit]


def from_base(value, unit):
    """
    Convert stress value from base unit (Pascals) to specified unit.
    
    Args:
        value: Stress value in Pascals
        unit: Target unit name (Pa, kPa, MPa, GPa, psi)
        
    Returns:
        Stress value in target unit
    """
    return value / STRESS_UNITS[unit]
