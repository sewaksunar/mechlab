# Architecture

mechlab is organized into four layers with a strict one-directional
dependency flow:

```
interfaces/   -> CLI, reports, plots        (user/system facing)
application/  -> workflow orchestration      (the public API)
engine/       -> solvers, units, math        (numerical machinery)
domain/       -> Body, Beam, Load, Material  (pure engineering science)
```

A layer may only import from layers **below** it. `domain/` never
imports from `engine/`; `engine/` never imports from `application/`.
This keeps the physics/math (`domain/`) unit-testable in complete
isolation, with no I/O, no mocks, no fixtures required.

## Design patterns

- **Abstract Base Class** — `Body` and `Load` define contracts that
  subclasses (`Beam`, `PointLoad`, `DistributedLoad`) must fulfill.
- **Strategy** — `EquilibriumSolver` is *composed into* `Beam` rather
  than inherited, so the solving algorithm can be swapped without
  touching the `Beam` class.
- **Facade** — `BeamAnalysis` hides domain/engine complexity behind a
  small, fluent public API.
- **Method chaining** — `add_load()`, `add_support()`, etc. return
  `self`, enabling a readable fluent interface.

## Extending mechlab

**Adding a new `Body` type (e.g. `Truss`):**

1. Create `domain/statics/truss.py`, subclass `Body`, implement `solve()`.
2. Reuse `EquilibriumSolver` from `engine/math/`, or add a new solver
   class there — keep solving algorithms out of `domain/`.
3. Add a facade method/class in `application/api.py`.
4. Wire a CLI subcommand in `interfaces/cli/commands.py` if needed.
5. Add tests under `tests/domain/`, `tests/engine/`, `tests/application/`.

**Adding a new unit:**

Call `UnitRegistry().register("symbol", si_factor)`, or add it to the
default table in `engine/units/registry.py`.
