class SimplySupportedBeam:
    def __init__(self, length, load, E, I):
        self.L = float(length)
        self.P = float(load)
        self.E = float(E)
        self.I = float(I)

        self._compute()

    def _compute(self):
        self.RA = self.P / 2
        self.RB = self.P / 2

        self.M_max = self.P * self.L / 4
        self.delta_max = (self.P * self.L**3) / (48 * self.E * self.I)

    def results(self):
        return {
            "Length (L)": self.L,
            "Load (P)": self.P,
            "Reaction A": self.RA,
            "Reaction B": self.RB,
            "Max Moment": self.M_max,
            "Max Deflection": self.delta_max,
        }

    def __repr__(self):
        return (
            f"SimplySupportedBeam(L={self.L}, P={self.P}, "
            f"E={self.E}, I={self.I})"
        )
