import sympy as sp

def show_stress(state):
    try:
        from IPython.display import display, Math
    except ImportError:
        raise RuntimeError("IPython not available")

    s1, s2 = state.principal_stresses()

    expr = sp.Matrix([
        sp.Symbol("σ₁") - s1,
        sp.Symbol("σ₂") - s2
    ])

    display(Math(sp.latex(expr)))
