"""Plane stress utilities.

Centralized stress-state calculations used by CLI, widgets, and API.
"""

from __future__ import annotations

import math
from mechlab.units import STRESS_UNITS, from_base, to_base


class StressState:
    """Plane stress state (σx, σy, τxy) with optional unit conversion."""

    def __init__(self, sx: float, sy: float, txy: float, unit: str | None = "MPa"):
        self._unit = unit
        self._validate_unit(unit)

        if unit is None:
            self._sx = float(sx)
            self._sy = float(sy)
            self._txy = float(txy)
        else:
            self._sx = to_base(float(sx), unit)
            self._sy = to_base(float(sy), unit)
            self._txy = to_base(float(txy), unit)

    @staticmethod
    def _validate_unit(unit: str | None) -> None:
        if unit is None:
            return
        if unit not in STRESS_UNITS:
            valid = ", ".join(sorted(STRESS_UNITS))
            raise ValueError(f"Unsupported unit '{unit}'. Use one of: {valid}.")

    def _to_unit(self, value: float, unit: str | None) -> float:
        if unit is None:
            return value
        self._validate_unit(unit)
        return from_base(value, unit)

    @property
    def unit(self) -> str | None:
        return self._unit

    @property
    def sigma_x(self) -> float:
        return self._to_unit(self._sx, self._unit)

    @property
    def sigma_y(self) -> float:
        return self._to_unit(self._sy, self._unit)

    @property
    def tau_xy(self) -> float:
        return self._to_unit(self._txy, self._unit)

    # Backward-compatible aliases
    @property
    def sx(self) -> float:
        return self.sigma_x

    @property
    def sy(self) -> float:
        return self.sigma_y

    @property
    def txy(self) -> float:
        return self.tau_xy

    def principal(self, unit: str | None = None) -> tuple[float, float]:
        """Return principal stresses (σ1, σ2)."""
        unit = self._unit if unit is None else unit
        avg = (self._sx + self._sy) / 2
        r = math.sqrt(((self._sx - self._sy) / 2) ** 2 + self._txy**2)
        return self._to_unit(avg + r, unit), self._to_unit(avg - r, unit)

    def principal_stresses(self, unit: str | None = None) -> tuple[float, float]:
        """Alias for :meth:`principal`."""
        return self.principal(unit)

    def max_shear(self, unit: str | None = None) -> float:
        """Return maximum shear stress (τmax)."""
        unit = self._unit if unit is None else unit
        r = math.sqrt(((self._sx - self._sy) / 2) ** 2 + self._txy**2)
        return self._to_unit(r, unit)

    def von_mises(self, unit: str | None = None) -> float:
        """Return Von Mises equivalent stress."""
        unit = self._unit if unit is None else unit
        value = math.sqrt(self._sx**2 - self._sx * self._sy + self._sy**2 + 3 * self._txy**2)
        return self._to_unit(value, unit)

    def results(self, unit: str | None = None) -> dict[str, float | str | None]:
        """Return a results dictionary in the requested unit."""
        unit = self._unit if unit is None else unit
        s1, s2 = self.principal(unit)
        return {
            "σx": self._to_unit(self._sx, unit),
            "σy": self._to_unit(self._sy, unit),
            "τxy": self._to_unit(self._txy, unit),
            "σ1": s1,
            "σ2": s2,
            "τmax": self.max_shear(unit),
            "von_mises": self.von_mises(unit),
            "unit": unit,
        }

    def __repr__(self) -> str:
        unit = self._unit or ""
        return (
            "StressState(σx={:.3f}, σy={:.3f}, τxy={:.3f}, "
            "σ1={:.3f}, σ2={:.3f}, τmax={:.3f}{})"
        ).format(
            self.sigma_x,
            self.sigma_y,
            self.tau_xy,
            *self.principal(),
            self.max_shear(),
            f" {unit}" if unit else "",
        )
