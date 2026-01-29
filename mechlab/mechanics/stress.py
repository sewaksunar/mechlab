import math

class StressState:
    def __init__(self, sx, sy, txy):
        self.sx = float(sx)
        self.sy = float(sy)
        self.txy = float(txy)

        self._compute()

    def _compute(self):
        self.s_avg = (self.sx + self.sy) / 2
        self.R = math.sqrt(((self.sx - self.sy) / 2) ** 2 + self.txy ** 2)

        self.s1 = self.s_avg + self.R
        self.s2 = self.s_avg - self.R
        self.tmax = self.R

    def results(self):
        return {
            "σx": self.sx,
            "σy": self.sy,
            "τxy": self.txy,
            "σ1": self.s1,
            "σ2": self.s2,
            "τmax": self.tmax,
        }

    def __repr__(self):
        return (
            f"StressState(σx={self.sx}, σy={self.sy}, τxy={self.txy}, "
            f"σ1={self.s1}, σ2={self.s2}, τmax={self.tmax})"
        )
