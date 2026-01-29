# mechlab/core/units.py

STRESS_UNITS = {
    "Pa": 1.0,
    "kPa": 1e3,
    "MPa": 1e6,
    "GPa": 1e9,
    "psi": 6894.76,
}

def to_base(value, unit):
    """Convert to Pascals"""
    return value * STRESS_UNITS[unit]

def from_base(value, unit):
    """Convert from Pascals"""
    return value / STRESS_UNITS[unit]
