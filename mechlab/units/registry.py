# Base units:
# length -> meter (m)
# force  -> newton (N)
# pressure -> pascal (Pa)
# mass -> kilogram (kg)

UNITS = {
    "length": {
        "m": 1.0,
        "mm": 1e-3,
        "cm": 1e-2,
        "km": 1e3,
        "inch": 0.0254,
        "ft": 0.3048,
    },
    "force": {
        "N": 1.0,
        "kN": 1e3,
        "MN": 1e6,
        "lbf": 4.44822,
    },
    "pressure": {
        "Pa": 1.0,
        "kPa": 1e3,
        "MPa": 1e6,
        "bar": 1e5,
        "psi": 6894.76,
    },
    "mass": {
        "kg": 1.0,
        "g": 1e-3,
        "ton": 1e3,
        "lb": 0.453592,
    },
}
