import numpy as np
import matplotlib.pyplot as plt

class BeamPlot:
    def __init__(self, beam):
        self.beam = beam

    def show(self):
        L = self.beam.L
        P = self.beam.P

        x = np.linspace(0, L, 200)

        # Shear force
        V = np.where(x < L/2, self.beam.RA, -self.beam.RB)

        # Bending moment
        M = np.where(
            x < L/2,
            self.beam.RA * x,
            self.beam.RA * x - P * (x - L/2)
        )

        fig, axs = plt.subplots(2, 1, figsize=(8, 6), sharex=True)

        axs[0].plot(x, V)
        axs[0].set_title("Shear Force Diagram")
        axs[0].set_ylabel("Shear")

        axs[1].plot(x, M)
        axs[1].set_title("Bending Moment Diagram")
        axs[1].set_ylabel("Moment")
        axs[1].set_xlabel("Length")

        for ax in axs:
            ax.grid(True)

        plt.tight_layout()
        plt.show()
