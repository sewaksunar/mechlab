<p align="center">
  <img src="https://github.com/sewaksunar/mechlab/blob/main/docs/source/_static/logo.png" width="200" alt="MechLab Logo">
</p>

![PyPI](https://img.shields.io/pypi/v/mechlab)
![License](https://img.shields.io/pypi/l/mechlab)
![Python](https://img.shields.io/pypi/pyversions/mechlab)
[![docs](https://github.com/3b1b/manim/workflows/docs/badge.svg)](https://sewaksunar.github.io/mechlab/)
<!-- [![MechLab Subreddit](https://img.shields.io/reddit/subreddit-subscribers/manim.svg?color=ff4301&label=reddit&logo=reddit)](https://www.reddit.com/r/) -->

# MechLab

**MechLab** is an open-source **Python library for mechanical engineering computations**, providing a unified, modular, and extensible toolkit for **students, researchers, and practicing engineers**.

It brings together widely used scientific libraries under a clean, engineering-focused API for:

`mechanics` `thermodynamics` `fluid mechanics` `control systems` `numerical & symbolic computation`

---

## Features

* Mechanics (statics & dynamics)
* Thermodynamics utilities (properties, processes, cycles)
* Fluid mechanics calculations (dimensionless numbers, flow relations)
* Control systems analysis
* Symbolic & numerical computation
* Modular and extensible architecture
* Sphinx-based documentation with API reference

---

## Installation

Install directly from **PyPI**:

```bash
pip install mechlab
```

Using **uv** (recommended):

```bash
uv pip install mechlab
```

---

## Quick Start

### Thermodynamics

```python
from mechlab.thermodynamics import enthalpy_TP

h = enthalpy_TP(
    fluid="Water",
    T=500,        # Temperature [K]
    P=3e6         # Pressure [Pa]
)
print(f"Enthalpy: {h:.2f} J/kg")
```

### Stress Analysis

```python
from mechlab.mechanics import StressState

# Create stress state
state = StressState(sx=100, sy=50, txy=30, unit="MPa")

# Get results
results = state.results()
print(f"Principal stress σ₁: {results['sigma_1']:.2f} MPa")
print(f"Von Mises stress: {results['von_mises']:.2f} MPa")
```

---

## Package Structure

```text
mechlab/
├── cli/                    # Command-line interface
├── core/                   # Base classes and unit conversions
├── display/                # Text and LaTeX output utilities
├── export/                 # CSV and PDF export tools
├── interactive/            # Jupyter notebook widgets
├── math/                   # Core engineering calculations
├── mechanics/              # Mechanics analysis
│   ├── beam.py             # Beam analysis
│   ├── stress.py           # Plane stress utilities
│   ├── statics/            # Static analysis models
│   └── dynamics/           # Dynamics models
├── thermodynamics/         # Thermodynamic calculations
├── units/                  # Unit registry and conversions
├── utils/                  # Environment detection utilities
├── visual/                 # Visualizations and animations
└── __init__.py
```

## Dependencies

MechLab is built on top of proven scientific Python libraries:

`numpy` `scipy` `sympy` `control` `fluids` `CoolProp` `pint` `matplotlib`

All dependencies are installed automatically.

---

## Design Philosophy

* **Engineering-first API** (clear physical meaning)
* **Readable code** over premature optimization
* **Modular design** — subject areas are independent
* **Extensible** — easy to add new models & correlations
* **Documented** — API reference generated directly from code

---

## Roadmap

* Rankine, Otto, Diesel cycles
* Pipe flow & heat exchanger modules
* Full unit-aware API using Pint
* Validation against textbook examples
* Interactive Jupyter notebooks
* Hosted documentation website

---

## Development Setup (Contributors)

Clone the repository:

```bash
git clone https://github.com/sewaksunar/mechlab.git
cd mechlab
```

Create a virtual environment and install dependencies with **uv**:

```bash
uv venv
uv pip install -e .
```

Build documentation:

```bash
cd docs
uv run sphinx-build source build
```

Run tests:

```bash
pytest
```

---

## Command Line Interface

MechLab includes a powerful CLI for quick calculations:

```bash
# Run interactive shell
mechlab shell

# System check
mechlab doctor

# Math calculations
mechlab math stress 1000 0.05  # stress = force / area

# Stress analysis
mechlab stress compute --sx 100 --sy 50 --txy 30
mechlab stress show --sx 100 --sy 50 --txy 30

# Beam analysis
mechlab beam compute --L 5 --P 1000 --E 200e9 --I 1e-6
```

**Troubleshooting (Windows):** If `mechlab` is not recognized, use:

```bash
uv run mechlab
# or
uv run python -m mechlab
```

---

## Contributing

Contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Open a Pull Request

Please follow:

* PEP-8 style
* Clear docstrings
* Basic tests for new features

---

## Documentation

The documentation is built using **Sphinx** with autodoc support.

Build locally:

```bash
cd docs
uv run sphinx-build source build
```

Then open:

```
docs/build/index.html
```

---

## License

This project is licensed under the **MIT License**.

---

## Author

**Sewak Sunar**
Mechanical Engineering Enthusiast & Python Developer

GitHub: [https://github.com/sewaksunar](https://github.com/sewaksunar)

---

## Acknowledgements

Inspired by mechanical engineering textbooks and the open-source scientific Python ecosystem.

If you find **MechLab** useful, please ⭐ the repository on GitHub!

---