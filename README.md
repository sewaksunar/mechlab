<div align="center">

# MechLab

**A modern Python framework for mechanical and structural engineering analysis**

Beam theory, matrix solvers, and engineering visualization — built on clean, typed, object-oriented Python.

[![Python](https://img.shields.io/badge/python-3.10+-3776AB?logo=python&logoColor=white)]()
[![License](https://img.shields.io/badge/license-MIT-success)]()
[![Build](https://img.shields.io/badge/build-passing-brightgreen)]()
[![Type Checked](https://img.shields.io/badge/type--checked-mypy-blue)]()
[![Code Style](https://img.shields.io/badge/code%20style-ruff-black)]()

[Quick Start](#quick-start) · [Features](#features) · [Architecture](#architecture) · [Docs](#documentation) · [Contributing](#contributing)

</div>

---

## Table of Contents

- [Overview](#overview)
- [Why MechLab](#why-mechlab)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Documentation](#documentation)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

**MechLab** is an object-oriented Python framework for mechanical and structural engineering. It provides reusable engineering models, numerical solvers, and visualization tools for analyzing beams and structural systems — all built on a clean, modular architecture that scales from a quick hand-calc check to a full analysis pipeline.

The project is built around five principles:

| Principle | What it means in practice |
|---|---|
| **Domain-driven design** | Materials, sections, loads, and supports are first-class objects — not dictionaries or magic numbers |
| **Modern Python** | Python 3.10+, full type hints, `pyproject.toml`-based packaging |
| **Numerical accuracy** | Solvers validated against textbook and closed-form solutions |
| **Type safety** | Fully typed codebase, checked with `mypy` |
| **Extensibility** | Swap solvers, add element types, or plug in your own visualization backend |

---

## Why MechLab

Most engineers reach for a spreadsheet or a monolithic legacy tool for beam analysis. MechLab exists for the space in between — when you need **more rigor than a spreadsheet** but **more speed and transparency than a black-box FEA package**.

- **Readable models** — a `Material`, `Section`, or `Load` reads like the engineering concept it represents
- **Unit-aware** — SI units throughout, with explicit conversions where needed
- **Composable** — build up a beam from supports and loads, then swap the solver without touching your model
- **Visual by default** — FBD, SFD, BMD, and deflection curves are one call away

---

## Features

### 🔧 Engineering Models
- Materials (elastic modulus, yield strength, density)
- Cross-sections (area, moment of inertia, section modulus)
- Supports (pin, roller, fixed)
- Loads (point, distributed, moment)
- Beam elements composed from the above

### 📐 Analysis
- Static equilibrium checks
- Matrix-based beam solver
- Reaction force computation
- Internal shear and moment diagrams
- Deflection analysis (double integration / matrix methods)

### 📊 Visualization
- Free Body Diagrams (FBD)
- Shear Force Diagrams (SFD)
- Bending Moment Diagrams (BMD)
- Deflection curves

### 🏗️ Software Design
- Fully typed, `mypy`-checked codebase
- Object-oriented, modular architecture
- Unit-aware calculations throughout
- Extensive test coverage against known solutions

---

## Installation

Install the core package with [uv](https://github.com/astral-sh/uv):

```bash
uv add mechlab
```

Install with visualization support (matplotlib-based plotting):

```bash
uv sync --extra plots
```

> Prefer `pip`? `pip install mechlab` works too — `uv` is just faster.

---

## Quick Start

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
    area=2.3e-3,                # m²
    moment_of_inertia=9.19e-6,  # m⁴
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

---

## Architecture

MechLab follows a layered architecture — each layer depends only on the layer below it, keeping the domain models decoupled from both the solver internals and the public API.

```text
                    User
                      │
                      V
          ┌───────────────────────┐
          │   Application API     │   public workflows, user-facing classes
          └───────────+───────────┘
                      │
                      V
          ┌───────────────────────┐
          │   Solver Engine       │   numerical computation, matrix assembly
          └───────────+───────────┘
                      |
                      V
          ┌───────────────────────┐
          │   Domain Models       │   materials, sections, loads, supports
          └───────────+───────────┘
                      │
                      V
          ┌───────────────────────┐
          │   Shared Utilities    │   units, math helpers, validation
          └───────────────────────┘
```

| Layer | Responsibility |
|---|---|
| **Application** | Public API surface and end-to-end analysis workflows |
| **Engine** | Numerical solvers — matrix assembly, equilibrium solving |
| **Domain** | Engineering entities: materials, sections, loads, supports, beams |
| **Shared** | Cross-cutting utilities: unit handling, validation, math helpers |

---

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

---

## Documentation

Full documentation is available at **[username.github.io/mechlab](https://username.github.io/mechlab)**, organized into:

- **User Guide:**:  core concepts and workflows
- **Tutorials:** step-by-step worked examples
- **API Reference:** complete class and method reference
- **Mathematical Background:** the theory behind each solver

---

## Roadmap

### ✅ Current
- Beam analysis
- Materials & sections
- Loads & supports

### 🚧 Planned
- Truss analysis
- Frame analysis
- Full FEM support
- Dynamic (modal) analysis
- Buckling analysis
- Composite materials

Have a feature request? Open an issue — roadmap priorities are shaped by community input.

---

## Contributing

Contributions are welcome, whether it's a bug fix, a new feature, or a documentation improvement.

Please read **[CONTRIBUTING.md](CONTRIBUTING.md)** before opening an issue or pull request.

```bash
git clone https://github.com/your-username/mechlab.git
cd mechlab

uv sync
pytest
```

---

## License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for details.

---

<div align="center">

**Designed for engineers. Built with Python.**

</div>