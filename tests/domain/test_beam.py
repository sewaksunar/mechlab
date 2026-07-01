"""
Domain-layer tests. These should run fast and never touch disk/network
— they only exercise pure classes (Material, Section, Load, Beam).
"""

import pytest

from mechlab.domain.entities import (
    DistributedLoad,
    Material,
    PointLoad,
    Section,
    Support,
    SupportType,
)
from mechlab.domain.strength.beam import Beam


def make_beam() -> Beam:
    material = Material("steel", young_modulus=200e9, yield_strength=250e6)
    section = Section("I-beam", moment_of_inertia=9.19e-6, area=2.3e-3,
                       extreme_fiber_distance=0.076)
    beam = Beam(length=4.0, material=material, section=section)
    beam.add_support(Support(0.0, SupportType.PIN))
    beam.add_support(Support(4.0, SupportType.ROLLER))
    return beam


def test_material_rejects_nonpositive_modulus():
    with pytest.raises(ValueError):
        Material("bad", young_modulus=0, yield_strength=250e6)


def test_point_load_total_force():
    load = PointLoad(position=2.0, magnitude=5000)
    assert load.total_force() == 5000


def test_distributed_load_total_force_and_centroid():
    load = DistributedLoad(start=0.0, end=4.0, intensity=1000)
    assert load.total_force() == 4000
    assert load.position == 2.0  # centroid of uniform load


def test_symmetric_point_load_gives_equal_reactions():
    beam = make_beam()
    beam.add_load(PointLoad(position=2.0, magnitude=5000))
    beam.solve()
    reactions = dict(beam.reactions())
    assert reactions[0.0] == pytest.approx(2500)
    assert reactions[4.0] == pytest.approx(2500)


def test_reactions_before_solve_raises():
    beam = make_beam()
    with pytest.raises(RuntimeError):
        beam.reactions()
