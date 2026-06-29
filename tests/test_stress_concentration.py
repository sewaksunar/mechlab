import numpy as np

from mechlab.design import SteppedCircularBarKt, plot_stepped_circular_bar


def test_compute_scalar_matches_reference_formula():
    model = SteppedCircularBarKt()
    value = model.compute(0.05, 2.0)
    expected = 1.200 + 0.860 * np.sqrt(10.0) - 0.022 * 10.0
    expected += (-1.805 - 0.346 * np.sqrt(10.0) - 0.038 * 10.0) * 0.5
    expected += (2.198 - 0.486 * np.sqrt(10.0) + 0.165 * 10.0) * 0.5**2
    expected += (-0.593 - 0.028 * np.sqrt(10.0) - 0.106 * 10.0) * 0.5**3
    assert np.isclose(value, expected, rtol=1e-9, atol=1e-9)


def test_compute_vectorized_returns_array_with_nans_for_invalid_region():
    model = SteppedCircularBarKt()
    values = model.compute(np.array([0.05, 0.5]), np.array([2.0, 1.01]))
    assert values.shape == (2,)
    assert np.isfinite(values[0])
    assert np.isnan(values[1])


def test_plot_wrapper_returns_figure_and_axes(tmp_path):
    fig, ax = plot_stepped_circular_bar(point=(0.05, 2.0), show=False, save_path=tmp_path / "kt.png")
    assert fig is not None
    assert ax is not None
    assert (tmp_path / "kt.png").exists()