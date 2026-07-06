# mechlab

A modular, object-oriented engineering mechanics library. This repo is
intended as a **reusable template** — the beam analysis is a working
example, but the architecture is designed to scale to statics, dynamics,
and thermodynamics modules the same way.

## Architecture

Four layers, strict one-directional dependency flow:

```
interfaces/   -> CLI, reports, plots        (user/system facing)
application/  -> workflow orchestration      (the public API)
engine/       -> solvers, units, math        (numerical machinery)
domain/       -> Body, Beam, Load, Material  (pure engineering science)
```

**Rule:** a layer may only import from layers *below* it in this list.
`domain/` never imports from `engine/`; `engine/` never imports from
`application/`, and so on. This is what makes `domain/` unit-testable
without pytest fixtures, mocks, or any I/O setup.

```
mechlab/
├── pyproject.toml
├── README.md / CHANGELOG.md / CONTRIBUTING.md / LICENSE
├── mkdocs.yml
├── .github/workflows/         # CI: lint + type check + test, docs deploy
├── .pre-commit-config.yaml
├── src/mechlab/
│   ├── __init__.py           # public API surface + architecture doc
│   ├── __main__.py           # `python -m mechlab`
│   ├── domain/
│   │   ├── entities.py       # Body (ABC), Material, Section, Load hierarchy, Support
│   │   └── strength/
│   │       └── beam.py       # Beam(Body) — concrete OOP subclass
│   ├── engine/
│   │   ├── math/solvers.py   # EquilibriumSolver (Strategy pattern)
│   │   └── units/registry.py # UnitRegistry — SI <-> other units
│   ├── application/
│   │   ├── api.py            # BeamAnalysis — the facade users import
│   │   ├── config.py         # AnalysisConfig — app-level thresholds/defaults
│   │   └── workflows.py      # multi-step analyses (e.g. design checks)
│   ├── interfaces/
│   │   ├── cli/commands.py   # `mechlab beam --length ...`
│   │   ├── output/report.py  # ReportGenerator
│   │   └── visual/plots.py   # shear/moment diagrams (optional matplotlib extra)
│   └── shared/
│       └── utils.py          # dependency-free helpers, usable anywhere
├── tests/                    # mirrors src/, one test dir per layer, 94% coverage
├── docs/                     # MkDocs source, auto-generates API ref from docstrings
└── examples/
    └── simply_supported_beam.py
```

## Install

```bash
pip install -e ".[dev]"
```

## Quick start (Python API)

```python
from mechlab import BeamAnalysis
from mechlab.domain.entities import Material, Section

steel = Material(name="Steel A36", young_modulus=200e9, yield_strength=250e6)
section = Section(name="W150x18", moment_of_inertia=9.19e-6, area=2.3e-3,
                   extreme_fiber_distance=0.076)

result = (
    BeamAnalysis(length=4.0, material=steel, section=section)
    .set_simple_supports(0.0, 4.0)
    .add_point_load(2.0, 5000)
    .add_distributed_load(0.0, 4.0, 1000)
    .run()
)

print(result["safety_factor"])
```

## Quick start (CLI)

```bash
python -m mechlab beam \
    --length 4.0 --E 200e9 --yield 250e6 \
    --I 9.19e-6 --area 2.3e-3 --c 0.076 \
    --support 0.0 --support 4.0 \
    --point-load 2.0 5000
```

## Running tests

```bash
uv run pytest --cov=mechlab --cov-report=term-missing
```

Tests are organized by layer (`tests/domain`, `tests/engine`,
`tests/application`, `tests/interfaces`, `tests/shared`) so you can see
exactly which architectural layer each test targets. Currently at 94% coverage.

## Linting & type checking

```bash
uv run ruff check src tests examples   # lint
uv run ruff check --fix                # auto-fix what's fixable
uv run mypy                            # type check
```

CI runs all three (plus tests) on every push/PR across Python 3.9–3.12.
See `.github/workflows/ci.yml`.

## Documentation

```bash
uv sync --extra docs
uv run mkdocs serve     # live preview, auto-reloads
```

Use `uv run mkdocs serve` while editing docs. Run `uv run mkdocs build`
only when you need a deployable static site.

The API reference is generated automatically from docstrings — see
`docs/reference/*.md`. Docs auto-deploy to GitHub Pages on push to
`main` via `.github/workflows/docs.yml`.

## Pre-commit hooks (optional but recommended)

```bash
uv run pre-commit install
```

Runs ruff + mypy + basic hygiene checks automatically before each commit.

## Extending the template

**Adding a new Body type (e.g. Truss):**
1. Create `domain/statics/truss.py`, subclass `Body`, implement `solve()`.
2. Reuse `EquilibriumSolver` from `engine/math/` if it fits, or add a
   new solver class there (keep solving algorithms out of `domain/`).
3. Add a facade method/class in `application/api.py`.
4. Wire a CLI subcommand in `interfaces/cli/commands.py` if needed.
5. Add tests under `tests/domain/`, `tests/engine/`, `tests/application/`.

**Adding a new unit:**
Call `UnitRegistry().register("symbol", si_factor)`, or add it to the
default table in `engine/units/registry.py`.

## Design patterns used

- **Abstract Base Class** — `Body`, `Load` define contracts subclasses must fulfill.
- **Strategy** — `EquilibriumSolver` is composed into `Beam`, not inherited, so solving algorithms are swappable.
- **Facade** — `BeamAnalysis` hides domain/engine complexity behind a fluent API.
- **Method chaining** — `add_load()`, `add_support()` etc. return `self` for a readable fluent interface.
