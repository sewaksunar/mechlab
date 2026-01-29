# mechlab/display/text.py
def show_stress_text(state):
    s1, s2 = state.principal()
    print("\nStress Results")
    print("-" * 30)
    print(f"\\sigma x  = {state.sx}")
    print(f"\\sigma y  = {state.sy}")
    print(f"\\tau xy = {state.txy}")
    print(f"\\sigma 1  = {s1:.2f}")
    print(f"\\sigma 2  = {s2:.2f}")
    print(f"VM  = {state.von_mises():.2f}")
