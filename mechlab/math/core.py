class MathError(Exception):
    pass


def stress(force: float, area: float) -> float:
    if area == 0:
        raise MathError("Area cannot be zero")
    return force / area


def strain(delta_length: float, length: float) -> float:
    if length == 0:
        raise MathError("Original length cannot be zero")
    return delta_length / length


def youngs_modulus(stress: float, strain: float) -> float:
    if strain == 0:
        raise MathError("Strain cannot be zero")
    return stress / strain


def pressure(force: float, area: float) -> float:
    if area == 0:
        raise MathError("Area cannot be zero")
    return force / area
