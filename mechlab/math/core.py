"""Core mathematical functions for engineering calculations."""


class MathError(Exception):
    """Exception raised for mathematical errors in calculations."""
    pass


def stress(force: float, area: float) -> float:
    """
    Calculate stress: σ = F / A.
    
    Args:
        force: Applied force
        area: Cross-sectional area
        
    Returns:
        Stress value
        
    Raises:
        MathError: If area is zero
    """
    if area == 0:
        raise MathError("Area cannot be zero")
    return force / area


def strain(delta_length: float, length: float) -> float:
    """
    Calculate strain: ε = ΔL / L.
    
    Args:
        delta_length: Change in length
        length: Original length
        
    Returns:
        Strain value (dimensionless)
        
    Raises:
        MathError: If length is zero
    """
    if length == 0:
        raise MathError("Original length cannot be zero")
    return delta_length / length


def youngs_modulus(stress: float, strain: float) -> float:
    """
    Calculate Young's modulus: E = σ / ε.
    
    Args:
        stress: Stress value
        strain: Strain value
        
    Returns:
        Young's modulus
        
    Raises:
        MathError: If strain is zero
    """
    if strain == 0:
        raise MathError("Strain cannot be zero")
    return stress / strain


def pressure(force: float, area: float) -> float:
    """
    Calculate pressure: P = F / A.
    
    Args:
        force: Applied force
        area: Area
        
    Returns:
        Pressure value
        
    Raises:
        MathError: If area is zero
    """
    if area == 0:
        raise MathError("Area cannot be zero")
    return force / area
