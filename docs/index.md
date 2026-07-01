# mechlab

A modular, object-oriented engineering mechanics library for statics,
dynamics, and mechanics-of-materials analysis.

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
    .run()
)
print(result["safety_factor"])
```

## Where to go next

- **[Getting Started](getting-started.md)** — install and run your first analysis
- **[Architecture](architecture.md)** — how the four layers fit together
- **[API Reference](reference/domain.md)** — auto-generated from docstrings
- **[CLI Reference](cli.md)** — command-line usage
