def test_imports_smoke():
    import mechlab
    assert mechlab.__version__


def test_stress_state_smoke():
    from mechlab.mechanics import StressState

    state = StressState(100, 50, 25, unit="MPa")
    results = state.results()
    assert results["σ1"] >= results["σ2"]
