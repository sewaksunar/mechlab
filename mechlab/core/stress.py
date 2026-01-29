# mechlab/core/stress.py
import math
from mechlab.core.units import to_base, from_base

class StressState:
    def __init__(self, sx, sy, txy, unit="MPa"):
        # store internally in Pa
        self.sx = to_base(sx, unit)
        self.sy = to_base(sy, unit)
        self.txy = to_base(txy, unit)

    def principal(self):
        avg = (self.sx + self.sy) / 2
        r = math.sqrt(((self.sx - self.sy)/2)**2 + self.txy**2)
        return avg + r, avg - r

    def von_mises(self):
        return math.sqrt(
            self.sx**2 - self.sx*self.sy + self.sy**2 + 3*self.txy**2
        )

    def results(self, unit="MPa"):
        s1, s2 = self.principal()
        return {
            "σx": from_base(self.sx, unit),
            "σy": from_base(self.sy, unit),
            "τxy": from_base(self.txy, unit),
            "σ1": from_base(s1, unit),
            "σ2": from_base(s2, unit),
            "von_mises": from_base(self.von_mises(), unit),
            "unit": unit
        }
