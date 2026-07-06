"""Application-layer test: exercises the public BeamAnalysis facade end-to-end."""
from mechlab import BeamAnalysis
from mechlab.domain.entities import Material, Section


def test_beam_analysis_end_to_end():
    steel = Material("steel", young_modulus=200e9, yield_strength=250e6)
    section = Section("I-beam", moment_of_inertia=9.19e-6, area=2.3e-3,
                       extreme_fiber_distance=0.076)

    result = (
        BeamAnalysis(length=4.0, material=steel, section=section)
        .set_simple_supports(0.0, 4.0)
        .add_point_load(2.0, 5000)
        .add_distributed_load(0.0, 4.0, 1000)
        .run()
    )

    assert result["max_bending_stress_Pa"] > 0
    assert result["safety_factor"] > 1  # beam should not yield in this example
    assert len(result["reactions"]) == 2


def test_beam_analysis_plot_bending_moment_diagram():
    try:
        import matplotlib  # noqa: F401
    except ImportError:
        return

    steel = Material("steel", young_modulus=200e9, yield_strength=250e6)
    section = Section("I-beam", moment_of_inertia=9.19e-6, area=2.3e-3,
                       extreme_fiber_distance=0.076)

    figure = (
        BeamAnalysis(length=4.0, material=steel, section=section)
        .set_simple_supports(0.0, 4.0)
        .add_point_load(2.0, 5000)
        .plot_bending_moment_diagram()
    )

    assert figure is not None


def test_beam_analysis_plot_bending_moment_diagram_exports_file(tmp_path):
    try:
        import matplotlib  # noqa: F401
    except ImportError:
        return

    steel = Material("steel", young_modulus=200e9, yield_strength=250e6)
    section = Section("I-beam", moment_of_inertia=9.19e-6, area=2.3e-3,
                       extreme_fiber_distance=0.076)
    output_path = tmp_path / "diagram.png"

    figure = (
        BeamAnalysis(length=4.0, material=steel, section=section)
        .set_simple_supports(0.0, 4.0)
        .add_point_load(2.0, 5000)
        .plot_bending_moment_diagram(save_path=output_path)
    )

    assert figure is not None
    assert output_path.exists()
