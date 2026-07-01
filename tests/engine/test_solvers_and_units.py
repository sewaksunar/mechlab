"""Engine-layer tests: solver correctness and unit conversion, in isolation."""

import pytest

from mechlab.domain.entities import PointLoad, Support, SupportType
from mechlab.engine.math.solvers import EquilibriumSolver
from mechlab.engine.units.registry import UnitRegistry


def test_solver_requires_exactly_two_supports():
    solver = EquilibriumSolver()
    with pytest.raises(ValueError):
        solver.solve_two_support_reactions(4.0, [], [Support(0.0, SupportType.PIN)])


def test_offcenter_load_gives_unequal_reactions():
    solver = EquilibriumSolver()
    s1, s2 = Support(0.0, SupportType.PIN), Support(4.0, SupportType.ROLLER)
    load = PointLoad(position=1.0, magnitude=4000)  # closer to s1
    solver.solve_two_support_reactions(4.0, [load], [s1, s2])
    assert s1.reaction_force > s2.reaction_force
    assert s1.reaction_force + s2.reaction_force == pytest.approx(4000)


def test_unit_registry_round_trip():
    ur = UnitRegistry()
    si = ur.to_si(50, "kN")
    assert si == 50000.0
    assert ur.from_si(si, "kN") == pytest.approx(50)


def test_unit_registry_unknown_unit_raises():
    ur = UnitRegistry()
    with pytest.raises(ValueError):
        ur.to_si(1, "banana")
