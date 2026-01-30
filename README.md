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

```python
from mechlab.thermodynamics import enthalpy_TP

h = enthalpy_TP(
    fluid="Water",
    T=500,        # Temperature [K]
    P=3e6         # Pressure [Pa]
)

print(f"Enthalpy: {h:.2f} J/kg")
```

---

## Package Structure

```text
mechlab/
│
├── examples/              # Runnable example scripts
├── api.py                  # High-level API helpers
├── cli/                    # CLI entrypoints and subcommands
├── core/                   # Core math + unit helpers
├── display/                # Text/LaTeX/interactive display
├── export/                 # CSV/PDF export helpers
├── interactive/            # Jupyter widgets
├── math/                   # Math utilities
├── mechanics/              # Mechanics models
│   ├── stress.py           # Plane stress utilities
│   ├── statics/            # Statics models
│   └── dynamics/           # Dynamics models
├── thermodynamics/         # Thermodynamics utilities
├── units/                  # Unit registry + conversions
├── utils/                  # Environment + misc helpers
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

## CLI Troubleshooting (Windows)

If `mechlab` is not recognized, ensure the project is installed and prefer:

```bash
uv run mechlab
```

Or:

```bash
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