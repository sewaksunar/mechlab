# MechLab Library Structure

## Design Principles

1. **Single Source of Truth** – Each concept lives in one place only
2. **No Redundancy** – No duplicate code or overlapping modules
3. **Registry Pattern** – Auto-discovery and factory creation for physics objects
4. **Unified Animation** – One `animate()` function works with ANY physics object
5. **Lazy Loading** – Optional dependencies don't block imports
6. **Clear Exports** – Every `__init__.py` has `__all__` and docstrings
7. **Type Hints** – All public APIs have annotations
8. **Backward Compatible** – Old names work via aliases

## Module Overview

| Module | Purpose | Key Exports |
|--------|---------|-------------|
| `mechlab.core` | Base classes, registry, protocols | `PhysicsObject`, `Registry`, `Animatable`, `config` |
| `mechlab.mechanics` | Stress, beams, dynamics | `StressState`, `Projectile`, `RigidBody` |
| `mechlab.visual` | **Unified** animation & visualization | `animate`, `StressViewer`, `Projection` |
| `mechlab.units` | Unit conversion (single source) | `UNITS`, `convert` |
| `mechlab.output` | Text display + file export | `print_stress`, `export_csv`, `export_pdf` |
| `mechlab.thermodynamics` | Thermodynamic properties | `State`, `Cycle` |
| `mechlab.math` | Basic engineering formulas | `stress`, `strain`, `youngs_modulus` |
| `mechlab.utils` | Environment helpers | `is_jupyter` |
| `mechlab.cli` | Command-line interface | (internal) |

## File Structure

```
mechlab/
├── __init__.py          # Package entry
├── __main__.py          # python -m mechlab
├── api.py               # High-level API
│
├── core/                # Foundation (NEW: registry, protocols)
│   ├── __init__.py
│   └── base.py          # Registry, PhysicsObject, Animatable, config
│
├── mechanics/
│   ├── __init__.py      # Exports StressState, beams
│   ├── stress.py        # StressState (plane stress)
│   ├── beam.py          # SimplySupportedBeam
│   ├── statics/
│   │   ├── __init__.py
│   │   └── stress.py    # StressTensor3D, StressTransform
│   └── dynamics/        # (NEW: unified with core)
│       └── __init__.py  # DynamicsOfParticle, Projectile, RigidBody
│
├── visual/              # CONSOLIDATED (was 7 files → now 4)
│   ├── __init__.py      # Lazy exports with aliases
│   ├── animator.py      # BaseAnimator, PhysicsAnimator, animate(), Projection
│   ├── viewer.py        # StressViewer, StressAnimation (merged)
│   ├── beam.py          # BeamPlot
│   └── widgets.py       # stress_widget (Jupyter)
│
├── units/
│   ├── __init__.py
│   ├── registry.py      # Unit definitions
│   └── convert.py       # convert() function
│
├── output/
│   ├── __init__.py
│   ├── text.py          # print_stress, print_results
│   ├── csv.py           # export_csv
│   └── pdf.py           # export_pdf
│
├── thermodynamics/
│   ├── __init__.py
│   ├── state.py
│   ├── properties.py
│   └── cycle.py
│
├── math/
│   ├── __init__.py
│   └── core.py          # Basic formulas
│
├── utils/
│   ├── __init__.py
│   └── env.py           # is_jupyter()
│
└── cli/
    ├── __init__.py
    ├── __main__.py
    ├── common.py
    ├── stress.py
    ├── beam.py
    ├── units.py
    ├── math.py
    ├── doctor.py
    └── shell.py

examples/
├── __init__.py
├── demo.py              # Comprehensive demo (run this!)
├── plane_stress.py      # Simple stress example
├── stress_transform.py  # Symbolic 3D transformation
└── units.py             # Unit conversion examples

tests/
└── test_smoke.py        # Basic import tests
```

## Architecture Highlights

### 1. Registry Pattern
```python
from mechlab.core import physics_registry

# Auto-discovery of registered classes
physics_registry.list()  # ['projectile', 'rigid_body']

# Factory creation
proj = physics_registry.create("projectile", velocity=(20, 20, 0))
```

### 2. Unified Animation
```python
from mechlab.mechanics.dynamics import Projectile
from mechlab.visual import animate

# ONE function works with ANY Animatable object
proj = Projectile(velocity=(20, 20, 0))
anim = animate(proj)  # Auto-selects PhysicsAnimator
anim.preview()        # Interactive display
anim.save_gif("out.gif")  # Export
```

### 3. Protocol-Based Design
```python
from mechlab.core import Animatable

# Any object implementing these methods works with animate()
class MyPhysics:
    def state_at_time(self, t: float) -> PhysicsState: ...
    def time_span(self) -> tuple[float, float]: ...
```

### 4. Mixin Composition
```python
from mechlab.core import PhysicsObject, AnimatableMixin, ExportableMixin

class Projectile(PhysicsObject, AnimatableMixin, ExportableMixin):
    # Automatically gets: to_csv(), to_json(), trajectory(), etc.
    pass
```

## Quick Reference

```python
# Projectile motion with animation
from mechlab.mechanics.dynamics import Projectile
from mechlab.visual import animate

proj = Projectile(velocity=(20, 20, 0), mass=1.0)
print(f"Range: {proj.range():.2f} m")
anim = animate(proj)
anim.save_gif("projectile.gif")

# Stress analysis
from mechlab.mechanics import StressState
state = StressState(100, 50, 25)  # MPa
print(state.results())

# Interactive stress viewer
from mechlab.visual import StressViewer
StressViewer(100, 50, 25).show()

# 3D projection animation
from mechlab.visual import animate_cube
animate_cube(save="cube.gif")

# Unit conversion
from mechlab.units import convert
convert(100, 'MPa', 'psi')  # → 14503.77
```

## CLI Commands

```bash
mechlab stress compute --sx 100 --sy 50 --txy 25
mechlab beam compute --L 5 --P 1000 --E 200e9 --I 1e-4
mechlab units convert 100 MPa psi
mechlab doctor
```

## Files Removed (Cleanup)

The following redundant files were consolidated:
- `visual/animation.py` → merged into `viewer.py`
- `visual/projection.py` → merged into `animator.py`
- `visual/projectile_animation.py` → replaced by `animator.py`
- `test/mechanism.py`, `test/projectile.py` → removed (duplicates)
- `examples/projectile_motion_example.py` → consolidated into `demo.py`

## Adding New Physics Types

To add a new animatable physics object:

```python
from mechlab.core import PhysicsObject, AnimatableMixin, physics_registry, PhysicsState

@physics_registry.register("pendulum")
class Pendulum(PhysicsObject, AnimatableMixin):
    def __init__(self, length: float, angle0: float):
        super().__init__("Pendulum")
        self.length = length
        self.angle0 = angle0
    
    def state_at_time(self, t: float) -> PhysicsState:
        # Calculate position/velocity at time t
        ...
    
    def time_span(self) -> tuple[float, float]:
        return (0.0, 10.0)  # 10 second animation

# Now automatically works:
from mechlab.visual import animate
pendulum = Pendulum(1.0, 0.5)
anim = animate(pendulum)  # Just works!
```
