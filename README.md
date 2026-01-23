![PyPI](https://img.shields.io/pypi/v/mechlab)
![License](https://img.shields.io/pypi/l/mechlab)
![Python](https://img.shields.io/pypi/pyversions/mechlab)

# MechLab
<p align="center">
  <img src="https://github.com/sewaksunar/mechlab/blob/main/docs/source/_static/logo.png" width="200" alt="MechLab Logo">
</p>

**MechLab** is an open‑source Python library for **mechanical engineering computations**, designed to provide a unified, modular, and extensible toolkit for students, researchers, and practicing engineers.

It brings together commonly used scientific libraries under a clean, engineering‑focused API for **thermodynamics, fluid mechanics, control systems, and numerical analysis**.

---

## Fatures

* Thermodynamics utilities (properties, processes, cycles)
* Fluid mechanics calculations (dimensionless numbers, flow relations)
* Control systems support
* Symbolic & numerical computation
* Unit‑safe calculations (planned)
* Modular structure (easy to extend)

---

## Istallation

Install directly from **PyPI**:

```bash
pip install mechlab
```

Or using **Poetry**:

```bash
poetry add mechlab
```

---

## Quick Start

```python
from mechlab.thermodynamics import enthalpy_TP

h = enthalpy_TP(
    fluid="Water",
    T=500,        # Temperature in K
    P=3e6         # Pressure in Pa
)

print(f"Enthalpy: {h:.2f} J/kg")
```

---

## Package Structure

```text
mechlab/
│
├── thermodynamics/
│   ├── __init__.py
│   ├── properties.py
│   └── cycles.py
│
├── fluid_mechanics/
│   ├── __init__.py
│   └── dimensionless.py
│
├── control_systems/
│   ├── __init__.py
│   └── linear.py
│
├── utils/
│   ├── __init__.py
│   └── constants.py
│
└── __init__.py
```

---

## Dependencies

MechLab is built on top of proven scientific libraries:

`numpy`,  `scipy`, `sympy`, `control`, `fluids`, `CoolProp`, `pint`, `matplotlib`

These are installed automatically with MechLab.

---

## Design Philosophy

* **Engineering‑first API** (clear variable names, physical meaning)
* **Readable code** over premature optimization
* **Modular** – each subject area is independent
* **Extensible** – easy to add new models & correlations

---

## Roadmap

* [ ] Rankine, Otto, Diesel cycles
* [ ] Pipe flow & heat exchanger modules
* [ ] Full unit‑aware API using Pint
* [ ] Validation against textbook examples
* [ ] Interactive Jupyter examples
* [ ] Documentation website

---

## Development Setup

Clone the repository:

```bash
git clone https://github.com/sewaksunar/mechlab.git
cd mechlab
```

Install dependencies with Poetry:

```bash
poetry install
poetry shell
```

Run tests:

```bash
pytest
```

---

## Contributing

Contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Open a Pull Request

Please follow:

* PEP‑8 style
* Clear docstrings
* Basic tests for new features

---

## License

This project is licensed under the **MIT License**.

---

## Author

**Sewak Sunar**
Mechanical Engineering Enthusiast & Python Developer

* GitHub: [https://github.com/sewaksunar](https://github.com/sewaksunar)

---

## Acknowledgements

Inspired by mechanical engineering textbooks and the open‑source scientific Python ecosystem.

If you find MechLab useful, please ⭐ the repository on GitHub!
