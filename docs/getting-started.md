# Getting Started

Get **MechLab** installed in just a few minutes and run your first structural analysis.

---

## Installation

Install the latest stable release from PyPI.

![PyPI](https://img.shields.io/pypi/v/mechlab.svg?style=flat-square)

=== "pip"

    ```bash
    pip install mechlab
    ```

=== "uv"

    ```bash
    uv pip install mechlab
    ```

=== "Development"

    Clone the repository and install the development dependencies.

    ```bash
    uv sync --extra dev
    ```

!!! tip "Using uv?"
    `uv` is a fast Python package manager and drop-in replacement for many `pip` workflows.

---

## Verify the Installation

After installation, verify that MechLab is available.

=== "Python"

    ```python
    import mechlab

    print(mechlab.__version__)
    ```

    **Output**

    ```text
    0.1.0
    ```

=== "CLI"

    ```bash
    python -m mechlab --version
    ```

    **Output**

    ```text
    mechlab 0.1.0
    ```

!!! success
    If a version number is displayed, MechLab has been installed successfully.

---

## Your First Analysis

The example below creates a simply supported beam, applies both a point load and a uniformly distributed load, and runs the analysis.

```python
from mechlab import BeamAnalysis
from mechlab.domain.entities import Material, Section

steel = Material(
    name="Steel A36",
    young_modulus=200e9,
    yield_strength=250e6,
)

section = Section(
    name="W150x18",
    moment_of_inertia=9.19e-6,
    area=2.3e-3,
    extreme_fiber_distance=0.076,
)

analysis = (
    BeamAnalysis(length=4.0, material=steel, section=section)
    .set_simple_supports(pos_a=0.0, pos_b=4.0)
    .add_point_load(position=2.0, magnitude=5000)
    .add_distributed_load(
        start=0.0,
        end=4.0,
        intensity=1000,
    )
)

report = analysis.run()

print(report)
```

---

## Command-Line Interface

You can also perform analyses directly from the command line.

```bash
uv run python -m mechlab beam \
  --length 4.0 \
  --E 200e9 \
  --yield 250e6 \
  --I 9.19e-6 \
  --area 2.3e-3 \
  --c 0.076 \
  --support 0.0 \
  --support 4.0 \
  --point-load 2.0 5000
```

!!! info
    See the [CLI Reference](cli.md) for the complete list of commands and options.

---

## Running the Test Suite

If you're contributing to MechLab or working from source, run the test suite with:

```bash
uv run pytest
```

---

## Next Steps

Now that MechLab is installed, you can:

- Learn the core API in the **User Guide**
- Explore the **CLI Reference**
- Browse practical examples and tutorials
- Start building structural analysis workflows with MechLab