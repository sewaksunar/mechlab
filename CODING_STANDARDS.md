# MechLab Coding Standards

Professional code organization guidelines for consistent, maintainable code across all modules.

---

## 1. Code Style & Formatting

### Line Length
- Maximum 100 characters per line
- Break long lines for readability

### Tool: Black
Format all Python files with Black:
```bash
uv run black mechlab/ tests/ examples/
```

### Tool: isort
Organize imports consistently:
```bash
uv run isort mechlab/ tests/ examples/
```

---

## 2. Import Organization

**Order (Standard to Local):**
1. `__future__` imports
2. Standard library (`sys`, `os`, `math`, etc.)
3. Third-party (`numpy`, `scipy`, `sympy`)
4. Local (`from mechlab.core import ...`)
5. Relative imports (within package)

**Example:**
```python
from __future__ import annotations

import math
import sys
from typing import Optional

import numpy as np
import scipy.optimize as opt
from sympy import symbols, simplify

from mechlab.core.units import STRESS_UNITS, to_base, from_base
from . import helper_module
```

---

## 3. Type Hints

### Required For:
- All public function parameters and returns
- Class properties and attributes
- Module-level constants

### Example:
```python
from typing import Optional, Union

def calculate_stress(force: float, area: float) -> float:
    """Calculate stress from force and area."""
    if area <= 0:
        raise ValueError("Area must be positive")
    return force / area

class StressState:
    """Plane stress state representation."""
    
    def __init__(
        self,
        sigma_x: float,
        sigma_y: float,
        tau_xy: float,
        unit: Optional[str] = "MPa",
    ) -> None:
        self.sigma_x: float = sigma_x
        self.sigma_y: float = sigma_y
        self.tau_xy: float = tau_xy
        self.unit: Optional[str] = unit
```

---

## 4. Docstring Format (Google Style)

### Module-level:
```python
"""Brief one-line description.

Longer description explaining purpose, main classes/functions,
and usage patterns if needed.
"""
```

### Function/Method:
```python
def calculate_principal_stress(
    sx: float,
    sy: float,
    txy: float,
) -> tuple[float, float]:
    """Calculate principal stresses from plane stress components.

    Args:
        sx: Normal stress in x-direction (Pa or base unit).
        sy: Normal stress in y-direction (Pa or base unit).
        txy: Shear stress (Pa or base unit).

    Returns:
        Tuple of (sigma_1, sigma_2) principal stresses.

    Raises:
        ValueError: If inputs are invalid.

    Example:
        >>> s1, s2 = calculate_principal_stress(100, 50, 25)
        >>> print(s1, s2)
        118.03, 31.97
    """
    ...
```

### Class-level:
```python
class StressState:
    """Represents a 2D plane stress state.

    This class manages stress components (σx, σy, τxy) with automatic
    unit conversion and provides methods for stress analysis.

    Attributes:
        sigma_x: Normal stress in x-direction.
        sigma_y: Normal stress in y-direction.
        tau_xy: Shear stress.
        unit: Unit system (e.g., 'MPa', 'Pa').
    """
```

---

## 5. Code Organization Within Files

### File Structure:
```python
# 1. Module docstring
"""Description of module purpose."""

# 2. __future__ imports
from __future__ import annotations

# 3. Standard library
import math
import sys

# 4. Third-party
import numpy as np

# 5. Local imports
from mechlab.core.units import STRESS_UNITS

# 6. Type definitions (if using typing)
from typing import TypeAlias

StressComponent: TypeAlias = float

# 7. Constants
TOLERANCE = 1e-6
MAX_ITERATIONS = 1000

# 8. Exception classes
class StressError(Exception):
    """Custom exception for stress calculations."""
    pass

# 9. Helper functions
def _validate_stress(stress: float) -> None:
    """Internal helper - prefix with underscore."""
    pass

# 10. Main classes
class StressState:
    """Public API class."""
    pass

# 11. Public functions
def calculate_stress(force: float, area: float) -> float:
    """Public API function."""
    pass

# 12. Module exports
__all__ = ["StressState", "calculate_stress"]
```

---

## 6. Naming Conventions

| Element | Style | Example |
|---------|-------|---------|
| Constants | `UPPER_SNAKE_CASE` | `MAX_ITERATIONS = 1000` |
| Variables | `lower_snake_case` | `stress_value = 100.0` |
| Functions | `lower_snake_case` | `def calculate_stress()` |
| Classes | `PascalCase` | `class StressState` |
| Private functions | `_leading_underscore` | `def _validate_input()` |
| Methods | `lower_snake_case` | `def get_principal_stress()` |
| Properties | `lower_snake_case` | `@property def sigma_x()` |

---

## 7. Class Design

### Properties vs Methods:
- Use `@property` for attributes (no computation)
- Use methods for operations

```python
class StressState:
    def __init__(self, sx: float, sy: float, txy: float) -> None:
        self._sx = sx
        self._sy = sy
        self._txy = txy

    @property
    def sigma_x(self) -> float:
        """Read-only property."""
        return self._sx

    def calculate_principal_stress(self) -> tuple[float, float]:
        """Method for computation."""
        ...
```

### Initialization:
```python
class StressState:
    """Always include type hints in __init__."""
    
    def __init__(
        self,
        sigma_x: float,
        sigma_y: float,
        tau_xy: float,
        unit: str | None = "MPa",
    ) -> None:
        """Initialize stress state.

        Args:
            sigma_x: Normal stress in x-direction.
            sigma_y: Normal stress in y-direction.
            tau_xy: Shear stress.
            unit: Unit system.
        """
        self._validate_inputs(sigma_x, sigma_y, tau_xy)
        self._sx = sigma_x
        self._sy = sigma_y
        self._txy = tau_xy
        self._unit = unit

    @staticmethod
    def _validate_inputs(sx: float, sy: float, txy: float) -> None:
        """Validate input parameters."""
        if not isinstance(sx, (int, float)):
            raise TypeError("sigma_x must be numeric")
        if not isinstance(sy, (int, float)):
            raise TypeError("sigma_y must be numeric")
        if not isinstance(txy, (int, float)):
            raise TypeError("tau_xy must be numeric")
```

---

## 8. Error Handling

### Custom Exceptions:
```python
class MechlabError(Exception):
    """Base exception for MechLab."""
    pass

class StressError(MechlabError):
    """Raised for stress calculation errors."""
    pass

class UnitError(MechlabError):
    """Raised for unit conversion errors."""
    pass
```

### Usage:
```python
def calculate_stress(force: float, area: float) -> float:
    """Calculate stress.
    
    Raises:
        StressError: If area is zero or negative.
    """
    if area <= 0:
        raise StressError(f"Area must be positive, got {area}")
    return force / area
```

---

## 9. Testing Standards

### Test Naming:
```python
# tests/test_<module>.py

def test_<functionality>_<condition>() -> None:
    """Test description."""
    # Arrange
    input_data = ...
    
    # Act
    result = function(input_data)
    
    # Assert
    assert result == expected_value
```

### Example:
```python
def test_stress_calculation_with_positive_values() -> None:
    """Test stress calculation returns correct value for valid inputs."""
    force = 1000.0
    area = 10.0
    expected = 100.0
    
    result = calculate_stress(force, area)
    
    assert result == expected

def test_stress_calculation_raises_error_for_zero_area() -> None:
    """Test stress calculation raises error when area is zero."""
    with pytest.raises(StressError):
        calculate_stress(1000.0, 0.0)
```

---

## 10. Validation & Enforcement

### Setup Tools
```bash
# Install dev dependencies
uv pip install black isort pytest pytest-cov mypy

# Format all code
uv run black mechlab/ tests/ examples/
uv run isort mechlab/ tests/ examples/

# Type check
uv run mypy mechlab/

# Run tests
uv run pytest tests/ --cov=mechlab
```

### Pre-commit (Optional, future)
```bash
uv pip install pre-commit
pre-commit install
```

---

## 11. Module Exports (`__all__`)

Every module should explicitly declare public API:

```python
# mechlab/mechanics/__init__.py
"""Mechanics module for statics and dynamics analysis."""

from .beam import Beam
from .stress import StressState, StressTransform
from .statics import RigidBody, StaticsParticle

__all__ = [
    "Beam",
    "StressState",
    "StressTransform",
    "RigidBody",
    "StaticsParticle",
]
```

---

## 12. Documentation Links

**Google Style Guide:**
https://google.github.io/styleguide/pyguide.html

**PEP 8:**
https://www.python.org/dev/peps/pep-0008/

**PEP 257 (Docstrings):**
https://www.python.org/dev/peps/pep-0257/

**Type Hints (PEP 484):**
https://www.python.org/dev/peps/pep-0484/

---

## Quick Reference

```bash
# Format code
uv run black mechlab/

# Sort imports
uv run isort mechlab/

# Type check
uv run mypy mechlab/

# Run all checks
uv run black mechlab/ && uv run isort mechlab/ && uv run pytest tests/
```
