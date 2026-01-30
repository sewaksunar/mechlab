"""Text-based display utilities for stress analysis."""


def show_stress_text(state):
    """
    Display stress analysis results in text format.
    
    Args:
        state: StressState object with stress values
    """
    s1, s2 = state.principal()
    print("\nStress Results")
    print("-" * 30)
    print(f"σ_x  = {state.sx}")
    print(f"σ_y  = {state.sy}")
    print(f"τ_xy = {state.txy}")
    print(f"σ_1  = {s1:.2f}")
    print(f"σ_2  = {s2:.2f}")
    print(f"VM   = {state.von_mises():.2f}")
