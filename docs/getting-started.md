# Getting Started

## Install

```bash
uv sync --extra dev
```

## Run your first analysis

```python
from mechlab import BeamAnalysis
from mechlab.domain.entities import Material, Section

steel = Material(name="Steel A36", young_modulus=200e9, yield_strength=250e6)
section = Section(name="W150x18", moment_of_inertia=9.19e-6, area=2.3e-3,
                   extreme_fiber_distance=0.076)

analysis = (
    BeamAnalysis(length=4.0, material=steel, section=section)
    .set_simple_supports(pos_a=0.0, pos_b=4.0)
    .add_point_load(position=2.0, magnitude=5000)
    .add_distributed_load(start=0.0, end=4.0, intensity=1000)
)

report = analysis.run()
print(report)
```

## Run tests

```bash
uv run pytest
```

## Use the CLI

```bash
uv run python -m mechlab beam --length 4.0 --E 200e9 --yield 250e6 --I 9.19e-6 --area 2.3e-3 --c 0.076 --support 0.0 --support 4.0 --point-load 2.0 5000
```

See the [CLI Reference](cli.md) for all options.
