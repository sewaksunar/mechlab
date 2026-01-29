# mechlab/mechanics/stress.py
import math
from mechlab.utils.env import is_jupyter

class StressState:
    def __init__(self, sx, sy, txy):
        self.sx = sx
        self.sy = sy
        self.txy = txy

    def principal_stress(self):
        avg = (self.sx + self.sy) / 2
        r = math.sqrt(((self.sx - self.sy) / 2) ** 2 + self.txy ** 2)
        return avg + r, avg - r

    def summary(self):
        s1, s2 = self.principal_stress()
        return {
            "σx": self.sx,
            "σy": self.sy,
            "τxy": self.txy,
            "σ1": round(s1, 3),
            "σ2": round(s2, 3),
        }

    def display(self, mode="auto"):
        if mode == "auto":
            mode = "widget" if is_jupyter() else "print"

        if mode == "print":
            self._print()

        elif mode == "plot":
            self._plot()

        elif mode == "widget":
            if not is_jupyter():
                raise RuntimeError("Widgets only work in Jupyter")
            from mechlab.interactive.stress_widget import stress_state_widget
            stress_state_widget(self)

        else:
            raise ValueError("mode must be print | plot | widget | auto")

    def _print(self):
        print("\nStress State")
        print("-" * 30)
        for k, v in self.summary().items():
            print(f"{k:>4} : {v}")

    def _plot(self):
        import matplotlib.pyplot as plt

        s1, s2 = self.principal_stress()
        plt.axhline(0)
        plt.scatter([0, 0], [s1, s2])
        plt.text(0, s1, f"σ1 = {s1:.2f}")
        plt.text(0, s2, f"σ2 = {s2:.2f}")
        plt.title("Principal Stresses")
        plt.show()
