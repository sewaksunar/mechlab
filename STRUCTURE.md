# Library Organization Summary

## Design Principles

1. **Single Source of Truth** – Each concept lives in one place only
2. **No Redundancy** – No duplicate code or overlapping modules
3. **Flat Structure** – Minimal nesting, direct imports
4. **Lazy Loading** – Optional dependencies don't block imports
5. **Clear Exports** – Every `__init__.py` has `__all__` and docstrings
6. **Type Hints** – All public APIs have annotations
7. **Backward Compatible** – Old module names work with deprecation warnings

## Module Overview

| Module | Purpose | Key Exports |
|--------|---------|-------------|
| `mechlab.mechanics` | Stress & structural analysis | `StressState`, `SimplySupportedBeam`, `Beam` |
| `mechlab.units` | Unit conversion (single source) | `UNITS`, `convert`, `STRESS_UNITS` |
| `mechlab.output` | Text display + file export | `print_stress`, `export_csv`, `export_pdf` |
| `mechlab.visual` | GUI, animations, Jupyter widgets | `StressViewer`, `StressAnimation`, `BeamPlot` |
| `mechlab.thermodynamics` | Thermodynamic properties | `State` |
| `mechlab.math` | Basic engineering formulas | `stress`, `strain`, `youngs_modulus` |
| `mechlab.core` | Base classes (re-exports units) | `EngineeringBase`, `STRESS_UNITS` |
| `mechlab.utils` | Environment helpers | `is_jupyter` |
| `mechlab.cli` | Command-line interface | (internal) |

> **Deprecated**: `display`, `export`, `interactive` → use `output` and `visual` instead

### 2. **Unified Code**
- Single `StressState` implementation in `mechlab.mechanics.stress`
- Backward-compatible re-export in `mechlab.core.stress`
- No duplicate stress workflows

### 3. **CLI Organization**
- Single entrypoint: `mechlab.cli.__main__.main()`
- Shared utilities in `mechlab.cli.common` (flag parsing)
- Individual command handlers for `stress`, `beam`, `units`, `math`, `doctor`, `shell`

### 4. **Examples**
- Organized in `examples/` folder with runnable scripts
- `plane_stress.py`: Basic plane stress calculations
- `stress_transform.py`: 3D symbolic and numeric transformations
- Clear README with usage commands

### 5. **Documentation**
- **Main index**: Reorganized with "Getting Started", "Learning & Reference", "Contribute & Explore"
- **API Reference**: Comprehensive mechanics reference
- **Examples**: Now fully integrated with Sphinx documentation
- **Guides**: Project structure guide explains modular design

### 6. **Import Safety**
- Lazy-loading for optional dependencies (`ipywidgets`, `reportlab`)
- Clean import with no circular dependencies
- All tests pass: `2 passed`

### 7. **Package & Build**
- ✅ Tests: 2/2 passing
- ✅ Docs: Build succeeded (no warnings)
- ✅ Package: `mechlab-0.2.4.tar.gz` and `.whl` built successfully
- ✅ Metadata: All checks pass

## File Structure

```
mechlab/
├── __init__.py          # Package entry, lazy deprecation warnings
├── __main__.py          # python -m mechlab entry
├── api.py               # High-level API (stress function)
│
├── mechanics/           # Core engineering calculations
│   ├── __init__.py      # Exports all classes
│   ├── stress.py        # StressState (plane stress)
│   ├── beam.py          # SimplySupportedBeam
│   ├── statics/         # Particle/beam statics, 3D tensors
│   │   ├── __init__.py
│   │   └── stress.py    # StressTensor3D, PrincipalStresses
│   └── dynamics/        # RigidBody dynamics
│       └── __init__.py
│
├── units/               # SINGLE source for all unit handling
│   ├── __init__.py      # Exports UNITS, convert, STRESS_UNITS
│   ├── registry.py      # Unit definitions + to_base/from_base
│   └── convert.py       # convert() function
│
├── output/              # Display & export (merged from display+export)
│   ├── __init__.py
│   ├── text.py          # print_stress, print_beam, print_results
│   ├── csv.py           # export_csv
│   └── pdf.py           # export_pdf (lazy-loaded)
│
├── visual/              # Visualization (merged from visual+interactive)
│   ├── __init__.py      # Lazy-loaded exports
│   ├── viewer.py        # StressViewer (Mohr's circle GUI)
│   ├── animation.py     # StressAnimation
│   ├── beam.py          # BeamPlot
│   └── widgets.py       # stress_widget (Jupyter)
│
├── thermodynamics/      # Thermo properties
│   ├── __init__.py
│   ├── state.py
│   ├── properties.py
│   └── cycle.py
│
├── math/                # Basic formulas
│   ├── __init__.py
│   └── core.py          # stress, strain, youngs_modulus
│
├── core/                # Base classes (re-exports units)
│   ├── __init__.py
│   └── base.py          # EngineeringBase, Number
│
├── utils/               # Helpers
│   ├── __init__.py
│   └── env.py           # is_jupyter()
│
└── cli/                 # Command-line interface
    ├── __init__.py
    ├── __main__.py      # Main entry
    ├── common.py        # Shared utilities
    ├── stress.py
    ├── beam.py
    ├── units.py
    ├── math.py
    ├── doctor.py
    └── shell.py
```

## Key Design Principles Applied

1. **Single Source of Truth**: All unit logic in `mechlab.units`, re-exported by `core`
2. **No Duplications**: Merged 6 visual/display files into 4 consolidated ones
3. **Clear Exports**: Every `__init__.py` has `__all__` and a docstring
4. **Lazy-Loading**: Optional dependencies don't block imports (ipywidgets, reportlab)
5. **Minimal Nesting**: Mechanics submodules kept flat where possible
6. **Type Hints**: All public APIs have type annotations
7. **Backward Compatibility**: Old module names work with deprecation warnings

## Quick Reference

```python
# Stress analysis
from mechlab.mechanics import StressState
state = StressState(100, 50, 25)  # σx, σy, τxy in MPa
state.principal()                  # → (110.35, 39.65)
state.von_mises()                  # → 96.82

# Unit conversion
from mechlab.units import convert
convert(100, 'MPa', 'psi')         # → 14503.77

# Output
from mechlab.output import print_stress, export_csv
print_stress(state)
export_csv(state.results(), 'out.csv')

# Visualization
from mechlab.visual import StressViewer
StressViewer(100, 50, 25).show()
```

## CLI Commands

```bash
# Get help
mechlab --help
mechlab stress --help
mechlab beam --help

# Stress analysis
mechlab stress compute --sx 100 --sy 50 --txy 25
mechlab stress compute --sx 100 --sy 50 --txy 25 --csv results.csv
mechlab stress show --sx 100 --sy 50 --txy 25
mechlab stress export --sx 100 --sy 50 --txy 25 --gif stress.gif

# Beam analysis
mechlab beam compute --L 5 --P 1000 --E 200e9 --I 1e-4
mechlab beam show --L 5 --P 1000 --E 200e9 --I 1e-4

# Unit conversion
mechlab units list
mechlab units convert 100 MPa psi

# Math functions
mechlab math list
mechlab math stress 1000 0.01

# System check
mechlab doctor
mechlab doctor --verbose
```

## Next Steps (Optional)

- Add unit tests for each module (currently only smoke tests)
- Set up GitHub Pages for hosted docs
- Add more beam types (cantilever, continuous)
- Add thermal stress analysis
