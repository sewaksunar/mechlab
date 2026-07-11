<p align="center">
    <a href="https://sewaksunar.github.io/mechlab"><img src="https://raw.githubusercontent.com/sewaksunar/mechlab/main/docs/source/_static/logo.png" alt="MechLab logo" width="220"></a>
    <br />
    <br />
    <a href="https://pypi.org/project/mechlab/"><img src="https://img.shields.io/pypi/v/mechlab.svg?style=flat&logo=pypi" alt="PyPI Latest Release"></a>
    <a href="https://github.com/sewaksunar/mechlab/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-red.svg?style=flat" alt="MIT License"></a>
    <a href="https://github.com/sewaksunar/mechlab/actions"><img src="https://img.shields.io/badge/build-passing-brightgreen" alt="Build"></a>
    <a href="https://mypy-lang.org/"><img src="https://img.shields.io/badge/type--checked-mypy-blue" alt="Type Checked"></a>
    <a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/badge/code%20style-ruff-black" alt="Code Style"></a>
    <a href="https://sewaksunar.github.io/mechlab"><img src="https://img.shields.io/badge/docs-passing-blue" alt="Documentation Status"></a>
    <a href="https://github.com/sewaksunar/mechlab/discussions"><img src="https://img.shields.io/badge/discussions-join-orange?logo=github" alt="GitHub Discussions"></a>
    <br />
    <br />
    <i>A modern Python library for mechanical engineering calculations.</i>
</p>
<hr />

**MechLab** is an object-oriented Python library for mechanical engineering calculations inluding finite element methods, matrix solvers, and engineering visualization, built on clean, typed, modern Python.

> [!NOTE]
> MechLab focuses on structural and beam analysis first. Materials, sections, loads, and supports are modeled as first-class typed objects rather than dictionaries or magic numbers, so results stay traceable from input to output.

## Table of Contents

- [Why MechLab](#why-mechlab)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Documentation](#documentation)
- [Help with MechLab](#help-with-mechlab)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [How to Cite MechLab](#how-to-cite-mechlab)
- [License](#license)

## Why MechLab

| Principle | What it means in practice |
|---|---|
| **Domain-driven design** | Materials, sections, loads, and supports are first-class objects |
| **Modern Python** | Python 3.10+, full type hints, `pyproject.toml`-based packaging |
| **Numerical accuracy** | Solvers validated against textbook and closed-form solutions |
| **Type safety** | Fully typed codebase, checked with `mypy` |
| **Extensibility** | Swap solvers, add element types, or plug in your own visualization backend |

## Features

**Engineering Models:**  materials, cross-sections, supports (pin, roller, fixed), loads (point, distributed, moment), and beam elements composed from the above.

**Analysis:**  static equilibrium checks, a matrix-based beam solver, reaction force computation, internal shear and moment diagrams, and deflection analysis via double integration or matrix methods.

**Visualization:**  free body diagrams (FBD), shear force diagrams (SFD), bending moment diagrams (BMD), and deflection curves.

**Software Design:**  fully typed and `mypy`-checked, object-oriented and modular, unit-aware throughout, with extensive test coverage against known solutions.

## Installation

> [!CAUTION]
> MechLab requires Python 3.10 or newer. If you're on an older interpreter, upgrade Python before installing.

Install the core package with [uv](https://github.com/astral-sh/uv):

```bash
uv add mechlab
```

Install with visualization support (matplotlib-based plotting):

```bash
uv sync --extra plots
```

> [!Note]
> Prefer `pip`? `pip install mechlab` works too but `uv` is just faster.

## Quick Start

The following is an example analysis you can run right away:

```python
from mechlab import Material, Section, Beam, Support, Load

# Define a material
steel = Material(
    name="Steel A36",
    young_modulus=200e9,   # Pa
    yield_strength=250e6,  # Pa
)

# Define a cross-section
section = Section(
    name="W150x18",
    area=2.3e-3,                # m^2
    moment_of_inertia=9.19e-6,  # m^4
)

# Build a simply supported beam with a midspan point load
beam = Beam(length=4.0, material=steel, section=section)
beam.add_support(Support.pin(at=0.0))
beam.add_support(Support.roller(at=4.0))
beam.add_load(Load.point(magnitude=-10e3, at=2.0))  # 10 kN downward

# Solve and inspect results
result = beam.solve()
print(result.reactions)
print(f"Max deflection: {result.max_deflection():.4f} m")

# Visualize
result.plot_bmd()
```

Save this as `example.py` and run it with `python example.py`. A bending moment diagram will render using the `plots` extra. You can find more worked examples in the [`examples/`](examples) directory, or visit the [tutorials](https://sewaksunar.github.io/mechlab/tutorial/) for step-by-step walkthroughs.

## Architecture

MechLab follows a layered architecture. Each layer depends only on the layer below it, keeping domain models decoupled from both solver internals and the public API.

```text
                    User
                      |
                      v
          +-----------------------+
          |   Application API     |   public workflows, user-facing classes
          +-----------------------+
                      |
                      v
          +-----------------------+
          |   Solver Engine       |   numerical computation, matrix assembly
          +-----------------------+
                      |
                      v
          +-----------------------+
          |   Domain Models       |   materials, sections, loads, supports
          +-----------------------+
                      |
                      v
          +-----------------------+
          |   Shared Utilities    |   units, math helpers, validation
          +-----------------------+
```

| Layer | Responsibility |
|---|---|
| **Application** | Public API surface and end-to-end analysis workflows |
| **Engine** | Numerical solvers — matrix assembly, equilibrium solving |
| **Domain** | Engineering entities: materials, sections, loads, supports, beams |
| **Shared** | Cross-cutting utilities: unit handling, validation, math helpers |

## Project Structure

```text
mechlab/
+--- src/
+   +--- mechlab/
+       +--- application/     # Public API and workflows
+       +--- domain/          # Materials, sections, loads, supports
+       +--- engine/          # Numerical solvers
+       +--- interfaces/      # Protocols / abstract base classes
+       +--- shared/          # Units, validation, math utilities
+       +--- __init__.py
+       +--- __main__.py
+
+--- docs/                     # User guide, tutorials, API reference
+--- examples/                 # Runnable example scripts
+--- tests/                    # Unit and validation tests
+--- .github/                  # CI workflows
+--- pyproject.toml
+--- README.md
+--- LICENSE
+--- CONTRIBUTING.md
```

## Documentation

Full documentation is available at **[Docs](https://sewaksunar.github.io/mechlab)**, organized into:

- **User Guide:** core concepts and workflows
- **Tutorials:** step-by-step worked examples
- **API Reference:** complete class and method reference

## Help with MechLab

If you need help installing or using MechLab, feel free to reach out on [GitHub Discussions](https://github.com/sewaksunar/mechlab/discussions). If you'd like to submit a bug report or feature request, please [open an issue](https://github.com/sewaksunar/mechlab/issues).

## Roadmap

**Current:**  beam analysis, materials & sections, loads & supports.

**Planned:**  truss analysis, frame analysis, full FEM support, dynamic (modal) analysis, buckling analysis, composite materials.

Have a feature request? Open an issue, roadmap priorities are shaped by community input.

## Contributing

Contributions are always welcome, whether it's a bug fix, a new feature, or a documentation improvement.

Please read **[CONTRIBUTING.md](CONTRIBUTING.md)** before opening an issue or pull request, and see the full guide at **[here](https://sewaksunar.github.io/mechlab/contributing)**.

Most development uses [`uv`](https://docs.astral.sh/uv/) for environment and dependency management, install it first, then follow the [development setup guide](https://sewaksunar.github.io/mechlab/contributing) in the docs.

## How to Cite MechLab

We acknowledge the importance of good software in supporting engineering research and practice. If MechLab supported your work, please cite it — this helps demonstrate its value and supports continued development. The recommended citation format is available via the "cite this repository" button on the [repository page](https://github.com/sewaksunar/mechlab).

<!-- ## Code of Conduct

Our full code of conduct, and how we enforce it, can be read in [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md). -->

## License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for details.

---

<div align="center">

**Designed for mechanical engineers. Built with Python.**

</div>