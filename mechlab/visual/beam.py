"""Beam diagram visualization."""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import matplotlib.pyplot as plt

if TYPE_CHECKING:
    from mechlab.mechanics.beam import SimplySupportedBeam


class BeamPlot:
    """
    Visualization for beam analysis.

    Creates shear force and bending moment diagrams.

    Example:
        >>> from mechlab.mechanics.beam import SimplySupportedBeam
        >>> beam = SimplySupportedBeam(5, 1000, 200e9, 1e-4)
        >>> BeamPlot(beam).show()
    """

    def __init__(self, beam: "SimplySupportedBeam") -> None:
        """
        Initialize beam plot.

        Args:
            beam: SimplySupportedBeam instance to visualize
        """
        self.beam = beam

    def _calculate_diagrams(self, n_points: int = 500):
        """Calculate shear and moment along beam."""
        L = self.beam.L
        P = self.beam.P
        
        x = np.linspace(0, L, n_points)
        
        # Shear force (point load at center)
        V = np.where(x < L / 2, self.beam.RA, -self.beam.RB)
        
        # Bending moment
        M = np.where(
            x < L / 2,
            self.beam.RA * x,
            self.beam.RA * x - P * (x - L / 2),
        )
        
        return x, V, M

    def show(self, figsize: tuple[float, float] = (10, 6)) -> None:
        """
        Display shear and moment diagrams.

        Args:
            figsize: Figure size (width, height) in inches
        """
        x, V, M = self._calculate_diagrams()
        
        fig, axs = plt.subplots(2, 1, figsize=figsize, sharex=True)
        
        # Shear force diagram
        axs[0].fill_between(x, V, alpha=0.3, color="blue")
        axs[0].plot(x, V, "b-", linewidth=2)
        axs[0].axhline(y=0, color="k", linewidth=0.5)
        axs[0].set_title("Shear Force Diagram", fontweight="bold")
        axs[0].set_ylabel("Shear Force (N)")
        axs[0].grid(True, alpha=0.3)
        
        # Bending moment diagram
        axs[1].fill_between(x, M, alpha=0.3, color="red")
        axs[1].plot(x, M, "r-", linewidth=2)
        axs[1].axhline(y=0, color="k", linewidth=0.5)
        axs[1].set_title("Bending Moment Diagram", fontweight="bold")
        axs[1].set_ylabel("Moment (N·m)")
        axs[1].set_xlabel("Position along beam (m)")
        axs[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()

    def save(self, filename: str = "beam_diagrams.png", dpi: int = 150) -> None:
        """
        Save diagrams to file.

        Args:
            filename: Output filename
            dpi: Image resolution
        """
        x, V, M = self._calculate_diagrams()
        
        fig, axs = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
        
        axs[0].fill_between(x, V, alpha=0.3, color="blue")
        axs[0].plot(x, V, "b-", linewidth=2)
        axs[0].axhline(y=0, color="k", linewidth=0.5)
        axs[0].set_title("Shear Force Diagram", fontweight="bold")
        axs[0].set_ylabel("Shear Force (N)")
        axs[0].grid(True, alpha=0.3)
        
        axs[1].fill_between(x, M, alpha=0.3, color="red")
        axs[1].plot(x, M, "r-", linewidth=2)
        axs[1].axhline(y=0, color="k", linewidth=0.5)
        axs[1].set_title("Bending Moment Diagram", fontweight="bold")
        axs[1].set_ylabel("Moment (N·m)")
        axs[1].set_xlabel("Position along beam (m)")
        axs[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(filename, dpi=dpi, bbox_inches="tight")
        plt.close(fig)
        print(f"✔ Saved to {filename}")
