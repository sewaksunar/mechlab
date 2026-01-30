"""LaTeX-based display utilities for Jupyter notebooks."""

import sympy as sp


def show_stress(state):
    """
    Display stress analysis results using LaTeX in Jupyter notebooks.
    
    Args:
        state: StressState object with stress values
        
    Raises:
        RuntimeError: If IPython is not available
    """
    try:
        from IPython.display import display, Math
    except ImportError:
        raise RuntimeError("IPython not available. This function requires Jupyter.")
    
    s1, s2 = state.principal_stresses()
    
    expr = sp.Matrix([
        sp.Symbol("σ₁") - s1,
        sp.Symbol("σ₂") - s2
    ])
    
    display(Math(sp.latex(expr)))
