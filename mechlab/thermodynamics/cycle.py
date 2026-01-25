
'''
Docstring for mechlab.thermodynamics.cycle
'''

'''
Air standard thermodynamic cycles: Otto, Diesel, and Dual cycles.
'''
class OtoCycle:
    '''
    Docstring for OtoCycle
    '''
    def __init__(self, compression_ratio, expansion_ratio, specific_heat_ratio):
        self.compression_ratio = compression_ratio
        self.expansion_ratio = expansion_ratio
        self.specific_heat_ratio = specific_heat_ratio

    def efficiency(self):
        r = self.compression_ratio
        k = self.specific_heat_ratio
        return 1 - (1 / (r ** (k - 1)))
    
    def pressure_after_compression(self, p1):
        r = self.compression_ratio
        k = self.specific_heat_ratio
        return p1 * r * (r**(k - 1)) / ((k-1)*(r-1))
    
    def mean_effective_pressure(self, p1, v1):
        r = self.compression_ratio
        k = self.specific_heat_ratio
        p2 = self.pressure_after_compression(p1)
        w_net = p2 * v1 * (1 - (1 / r**(k - 1)))
        v4 = v1
        v2 = v1 / r
        m_ep = w_net / (v4 - v2)
        return m_ep

class DieselCycle:
    def __init__(self, compression_ratio, cutoff_ratio, specific_heat_ratio):
        self.compression_ratio = compression_ratio
        self.cutoff_ratio = cutoff_ratio
        self.specific_heat_ratio = specific_heat_ratio

    def efficiency(self):
        r = self.compression_ratio
        rc = self.cutoff_ratio
        k = self.specific_heat_ratio
        return 1 - (1 / (r ** (k - 1))) * ((rc**k - 1) / (k * (rc - 1)))
    
    def pressure_after_compression(self, p1):
        r = self.compression_ratio
        k = self.specific_heat_ratio
        return p1 * r**k
    
    def work_output(self, p1, v1):
        r = self.compression_ratio
        rc = self.cutoff_ratio
        k = self.specific_heat_ratio
        v2 = v1 / r
        v3 = v2 * rc
        p2 = self.pressure_after_compression(p1)
        p3 = p2 * (rc ** k)
        w_net = (p3 * v3 - p2 * v2) - (p2 * v2 - p1 * v1)
        return w_net
    
    def mean_effective_pressure(self, p1, v1):
        w_net = self.work_output(p1, v1)
        v4 = v1
        v1_initial = v1
        v2 = v1 / self.compression_ratio
        m_ep = w_net / (v4 - v2)
        return m_ep
    
class DualCycle:
    def __init__(self, compression_ratio, cutoff_ratio, specific_heat_ratio, heat_addition_fraction):
        self.compression_ratio = compression_ratio
        self.cutoff_ratio = cutoff_ratio
        self.specific_heat_ratio = specific_heat_ratio
        self.heat_addition_fraction = heat_addition_fraction

    def efficiency(self):
        r = self.compression_ratio
        rc = self.cutoff_ratio
        k = self.specific_heat_ratio
        x = self.heat_addition_fraction
        term1 = 1 - (1 / (r ** (k - 1)))
        term2 = (x * (rc**k - 1) + (1 - x) * k * (rc - 1)) / (k * (rc - 1))
        return term1 * term2
    
    def pressure_after_compression(self, p1):
        r = self.compression_ratio
        k = self.specific_heat_ratio
        return p1 * r**k

'''
Fuel air cycles
'''


'''
Real cycles
'''