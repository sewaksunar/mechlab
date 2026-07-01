"""Tests for interfaces.visual.plots — plotting is optional (matplotlib extra)."""

from mechlab.domain.entities import Material, PointLoad, Section, Support, SupportType
from mechlab.domain.strength.beam import Beam
from mechlab.interfaces.visual.plots import plot_shear_moment


def _make_solved_beam() -> Beam:
    material = Material("steel", young_modulus=200e9, yield_strength=250e6)
    section = Section("I-beam", moment_of_inertia=9.19e-6, area=2.3e-3,
                       extreme_fiber_distance=0.076)
    beam = Beam(length=4.0, material=material, section=section)
    beam.add_support(Support(0.0, SupportType.PIN))
    beam.add_support(Support(4.0, SupportType.ROLLER))
    beam.add_load(PointLoad(2.0, 5000))
    beam.solve()
    return beam


def test_plot_shear_moment_returns_figure():
    matplotlib = pytest_importorskip_matplotlib()
    if matplotlib is None:
        return
    fig = plot_shear_moment(_make_solved_beam())
    assert fig is not None


def pytest_importorskip_matplotlib():
    try:
        import matplotlib  # noqa: F401
        return matplotlib
    except ImportError:
        return None
