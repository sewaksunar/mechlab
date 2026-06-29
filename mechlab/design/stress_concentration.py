"""Stress concentration factor design data and chart helpers.

This module turns the stepped circular tension-bar chart into a reusable
library component:

- vectorized Kt evaluation for scalars or arrays
- reusable design-curve metadata
- matplotlib plotting for reports and notebooks
- an interactive prompt for quick one-off use
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import numpy as np


@dataclass(frozen=True)
class DesignCurve:
    """Metadata for one design curve in the Kt chart."""

    D_over_d: float
    label: str
    label_x: float


@dataclass(frozen=True)
class SteppedCircularBarDesign:
    """Built-in curve definitions for the stepped circular tension bar chart."""

    curves: tuple[DesignCurve, ...] = (
        DesignCurve(3.0, "D/d = 3", 0.022),
        DesignCurve(2.0, "2", 0.030),
        DesignCurve(1.5, "1.5", 0.042),
        DesignCurve(1.2, "1.2", 0.062),
        DesignCurve(1.1, "1.1", 0.110),
        DesignCurve(1.05, "1.05", 0.155),
        DesignCurve(1.02, "1.02", 0.215),
        DesignCurve(1.01, "1.01", 0.265),
    )
    r_range: tuple[float, float] = (0.005, 0.30)
    dashed_r_range: tuple[float, float] = (0.012, 0.295)
    y_range: tuple[float, float] = (1.0, 5.0)


DEFAULT_CURVES = SteppedCircularBarDesign().curves
DEFAULT_R_RANGE = SteppedCircularBarDesign().r_range


class SteppedCircularBarKt:
    """Evaluate and plot Kt for a stepped circular tension bar.

    The implementation accepts scalars or NumPy arrays and returns values
    with the same shape, which makes it usable from scripts, notebooks, and
    higher-level design tools.
    """

    def __init__(self, design: SteppedCircularBarDesign | None = None) -> None:
        self.design = design or SteppedCircularBarDesign()

    @staticmethod
    def _as_array(value: float | Sequence[float] | np.ndarray) -> tuple[np.ndarray, bool]:
        array = np.asarray(value, dtype=float)
        scalar = array.ndim == 0
        if scalar:
            array = array.reshape(1)
        return array, scalar

    @staticmethod
    def _low_coefficients(t_over_r: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        root = np.sqrt(t_over_r)
        c1 = 0.926 + 1.157 * root - 0.099 * t_over_r
        c2 = 0.012 - 3.036 * root + 0.961 * t_over_r
        c3 = -0.302 + 3.977 * root - 1.744 * t_over_r
        c4 = 0.365 - 2.098 * root + 0.878 * t_over_r
        return c1, c2, c3, c4

    @staticmethod
    def _high_coefficients(t_over_r: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        root = np.sqrt(t_over_r)
        c1 = 1.200 + 0.860 * root - 0.022 * t_over_r
        c2 = -1.805 - 0.346 * root - 0.038 * t_over_r
        c3 = 2.198 - 0.486 * root + 0.165 * t_over_r
        c4 = -0.593 - 0.028 * root - 0.106 * t_over_r
        return c1, c2, c3, c4

    def compute(
        self,
        r_over_d: float | Sequence[float] | np.ndarray,
        D_over_d: float | Sequence[float] | np.ndarray,
    ) -> float | np.ndarray:
        """Compute Kt for scalar or array inputs.

        Returns NaN where the chart is out of range.
        """

        r_over_d_arr, r_scalar = self._as_array(r_over_d)
        D_over_d_arr, d_scalar = self._as_array(D_over_d)
        r_over_d_arr, D_over_d_arr = np.broadcast_arrays(r_over_d_arr, D_over_d_arr)

        with np.errstate(divide="ignore", invalid="ignore"):
            t_over_d = (D_over_d_arr - 1.0) / 2.0
            t_over_r = t_over_d / r_over_d_arr
            x = 2.0 * t_over_d / D_over_d_arr

        kt = np.full_like(t_over_r, np.nan, dtype=float)
        valid = np.isfinite(t_over_r) & (t_over_r >= 0.1) & (t_over_r <= 20.0)
        low = valid & (t_over_r <= 2.0)
        high = valid & (t_over_r > 2.0)

        if np.any(low):
            c1, c2, c3, c4 = self._low_coefficients(t_over_r[low])
            kt[low] = c1 + c2 * x[low] + c3 * x[low] ** 2 + c4 * x[low] ** 3

        if np.any(high):
            c1, c2, c3, c4 = self._high_coefficients(t_over_r[high])
            kt[high] = c1 + c2 * x[high] + c3 * x[high] ** 2 + c4 * x[high] ** 3

        if kt.size == 1 and (r_scalar or d_scalar):
            return float(kt[0])
        return kt

    def curve(self, D_over_d: float, r_over_d: np.ndarray) -> np.ndarray:
        """Convenience helper for one design curve."""

        values = self.compute(r_over_d, D_over_d)
        return np.asarray(values, dtype=float)

    def design_curves(
        self,
        r_over_d: np.ndarray | None = None,
        ratios: Sequence[float] | None = None,
    ) -> list[tuple[DesignCurve, np.ndarray, np.ndarray]]:
        """Return the data needed to plot the built-in design curves."""

        samples = np.asarray(
            r_over_d if r_over_d is not None else np.linspace(*self.design.r_range, 800),
            dtype=float,
        )
        selected = self.design.curves if ratios is None else tuple(
            curve for curve in self.design.curves if curve.D_over_d in ratios
        )

        series: list[tuple[DesignCurve, np.ndarray, np.ndarray]] = []
        for curve in selected:
            y_values = self.curve(curve.D_over_d, samples)
            mask = np.isfinite(y_values)
            series.append((curve, samples[mask], y_values[mask]))
        return series

    def plot(
        self,
        r_over_d: np.ndarray | None = None,
        ratios: Sequence[float] | None = None,
        point: tuple[float, float] | None = None,
        save_path: str | Path | None = None,
        show: bool = True,
        ax: plt.Axes | None = None,
    ) -> tuple[plt.Figure, plt.Axes]:
        """Plot the built-in design chart.

        Args:
            r_over_d: Optional x-axis samples.
            ratios: Optional subset of D/d curves to draw.
            point: Optional (r/d, D/d) point to mark on the chart.
            save_path: Optional image file to write.
            show: Whether to call plt.show().
            ax: Optional existing matplotlib axes.
        """

        if ax is None:
            fig, ax = plt.subplots(figsize=(8, 8))
        else:
            fig = ax.figure

        samples = np.asarray(
            r_over_d if r_over_d is not None else np.linspace(*self.design.r_range, 800),
            dtype=float,
        )

        for curve, x_values, y_values in self.design_curves(samples, ratios=ratios):
            ax.plot(x_values, y_values, color="black", linewidth=1.2)
            if len(x_values) and len(y_values):
                x_label = curve.label_x
                y_label = np.interp(x_label, x_values, y_values)
                ax.text(x_label, y_label + 0.05, curve.label, fontsize=8, ha="left", color="black")

        dashed_r = np.linspace(*self.design.dashed_r_range, 400)
        dashed_kt = self.compute(dashed_r, 1.0 + 2.0 * dashed_r)
        dashed_mask = np.isfinite(dashed_kt)
        ax.plot(dashed_r[dashed_mask], dashed_kt[dashed_mask], "k--", linewidth=1.0, dashes=(5, 3))
        if np.any(dashed_mask):
            x_loc = 0.18
            ax.text(
                x_loc,
                np.interp(x_loc, dashed_r[dashed_mask], dashed_kt[dashed_mask]) + 0.04,
                r"$r = \frac{D-d}{2}$",
                fontsize=9,
            )

        if point is not None:
            r_value, D_value = point
            kt_value = self.compute(r_value, D_value)
            if np.isfinite(kt_value):
                ax.plot(r_value, kt_value, "ro", markersize=8, zorder=5)
                ax.annotate(
                    f"  Kt = {kt_value:.3f}",
                    xy=(r_value, kt_value),
                    xytext=(r_value + 0.01, kt_value + 0.12),
                    fontsize=9,
                    color="red",
                    arrowprops=dict(arrowstyle="->", color="red", lw=1),
                )

        ax.set_xlim(*self.design.r_range)
        ax.set_ylim(*self.design.y_range)
        ax.set_xlabel(r"$r/d$", fontsize=13)
        ax.set_ylabel(r"$K_t$", fontsize=13, rotation=0, labelpad=10)
        ax.set_xticks(np.arange(0.0, 0.31, 0.05))
        ax.set_yticks(np.arange(1.0, 5.1, 0.5))
        ax.xaxis.set_minor_locator(MultipleLocator(0.01))
        ax.yaxis.set_minor_locator(MultipleLocator(0.1))
        ax.tick_params(which="both", direction="in", top=True, right=True)
        ax.tick_params(which="major", length=6)
        ax.tick_params(which="minor", length=3)
        ax.grid(True, which="major", color="#cccccc", linewidth=0.5)
        ax.grid(True, which="minor", color="#e5e5e5", linewidth=0.3)
        ax.set_title(
            "Chart 3.4 - Stress Concentration Factor $K_t$\n"
            "Stepped Tension Bar (Circular Cross Section)",
            fontsize=10,
            pad=10,
        )

        fig.tight_layout()
        if save_path is not None:
            fig.savefig(save_path, dpi=180, bbox_inches="tight")
        if show:
            plt.show()
        return fig, ax

    def prompt(self) -> float | np.ndarray:
        """Interactive prompt for quick one-off Kt evaluation."""

        print("-" * 40)
        r_over_d = float(input("Enter r/d  : "))
        D_over_d = float(input("Enter D/d  : "))
        kt_value = self.compute(r_over_d, D_over_d)
        if np.isnan(kt_value):
            print("WARNING: t/r out of valid range [0.1, 20.0]. Cannot compute Kt.")
        else:
            print(f"\n  Kt = {kt_value:.4f}\n")
        print("-" * 40)
        return kt_value


def plot_stepped_circular_bar(
    r_over_d: np.ndarray | None = None,
    ratios: Sequence[float] | None = None,
    point: tuple[float, float] | None = None,
    save_path: str | Path | None = None,
    show: bool = True,
    ax: plt.Axes | None = None,
) -> tuple[plt.Figure, plt.Axes]:
    """Functional wrapper around :class:`SteppedCircularBarKt`."""

    return SteppedCircularBarKt().plot(
        r_over_d=r_over_d,
        ratios=ratios,
        point=point,
        save_path=save_path,
        show=show,
        ax=ax,
    )