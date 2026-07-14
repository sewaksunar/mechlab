# relationship of dimensionalss group Fe/(V*Fr) and Fa/(V*Fr) for different bearing types
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
"""
F_a = axial load
F_r = radial load
F_e = equivalent radial load
V = rotation factor 
ordFe =Fe/(V*F_r)
ordFa = F_a/(V*F_r)
e = threshold value for the relationship between ordFe and ordFa
C0 = basic static load rating.
"""
def X_Y(e :float, Fa :float, C_0: float):
    if Fa/(C_0) < 0.0014:
        return ("X1 = 1.00, Y1 = 0, X2 = 0.56, Y2 = 2.30")
    if Fa/(C_0) == 0.002:
        return ("X1 = 1.00, Y1 = 0, X2 = 0.56, Y2 = 2.30")

def ordFe(Fa :float, Fr :float, V :float, e :float, X :float, Y :float) -> float:
    if Fa/(V*Fr) <= e:
        return 0.47
    else:
        return X + Y * (Fa/(V*Fr) - e)
    
import pandas as pd

# the hierarchical column headers (MultiIndex)
columns = pd.MultiIndex.from_tuples([
    ('Fa/C0', ''),
    ('e', ''),
    ('Fa/(VFr) <= e', 'X1'),
    ('Fa/(VFr) <= e', 'Y1'),
    ('Fa/(VFr) > e', 'X2'),
    ('Fa/(VFr) > e', 'Y2')
])

data = [
    [0.014,    0.19, 1.00, 0, 0.56, 2.30],
    [0.021,    0.21, 1.00, 0, 0.56, 2.15],
    [0.022,    0.22, 1.00, 0, 0.56, 1.99],
    [0.042,    0.24, 1.00, 0, 0.56, 1.85],
    [0.056,    0.26, 1.00, 0, 0.56, 1.71],
    [0.070,    0.27, 1.00, 0, 0.56, 1.63],
    [0.084,    0.28, 1.00, 0, 0.56, 1.55],
    [0.110,    0.30, 1.00, 0, 0.56, 1.45],
    [0.17,     0.34, 1.00, 0, 0.56, 1.31],
    [0.28,     0.38, 1.00, 0, 0.56, 1.15],
    [0.42,     0.42, 1.00, 0, 0.56, 1.04],
    [0.56,     0.44, 1.00, 0, 0.56, 1.00]
]

# table 11-4
df = pd.DataFrame(data, columns=columns)

# print(df)

# An SKF 6210 angular-contact ball bearing has an axial load Fa of 1779 N and a radial load Fr of 2224 N applied with the outer ring stationary. The basic static load rating C0 is 19793 N and the basic load rating C10 is 35139 N. Estimate the ℒ10 life at a speed of 720 rev/min.

Fa = 1779  # Axial load in N
C0 = 19793  # Basic static load rating in N
Fr = 2224 # radial load 

# calculating e form table (interpolating between the two closest values)
Fa_C0_calc = Fa / C0
# e = df.loc[df['Fa/C0'] >= Fa_C0_calc, 'e'].iloc[0] if not df.loc[df['Fa/C0'] >= Fa_C0_calc, 'e'].empty else df['e'].iloc[-1]
# print(f"Interpolated e value: {e}")

x_data = df[('Fa/C0', '')].values
e_data = df[('e', '')].values
y2_data = df[('Fa/(VFr) > e', 'Y2')].values

e_interp = np.interp(Fa_C0_calc, x_data, e_data)
print(f"Interpolated e : {e_interp:.3f}")

def choiceY(Fa, Fr, Fa_C0_calc, e_calc, df, V=1.0):
    x_data = df[('Fa/C0', '')].values
    
    #  the actual load ratio
    load_ratio = Fa / (V * Fr)
    
    #  condition is based on the load ratio vs e
    if load_ratio <= e_calc:
        # Returns Y1
        return np.interp(Fa_C0_calc, x_data, df[('Fa/(VFr) <= e', 'Y1')].values)
    else:
        # Returns the interpolated Y2 value
        return np.interp(Fa_C0_calc, x_data, df[('Fa/(VFr) > e', 'Y2')].values)
    
def choiceX(Fa, Fr, Fa_C0_calc, e_calc, df, V=1.0):
    x_data = df[('Fa/C0', '')].values
    
    # the actual load ratio
    load_ratio = Fa / (V * Fr)
    
    # condition is based on the load ratio vs e
    if load_ratio <= e_calc:
        # Returns X1
        return np.interp(Fa_C0_calc, x_data, df[('Fa/(VFr) <= e', 'X1')].values)
    else:
        # interpolated X2 value
        return np.interp(Fa_C0_calc, x_data, df[('Fa/(VFr) > e', 'X2')].values)

# Y2_interp = np.interp(Fa_C0_calc, x_data, y2_data)
Y_choice = choiceY(Fa=1779, Fr=Fr, Fa_C0_calc=Fa_C0_calc, e_calc=e_interp, df=df)
print(f"Interpolated Y2: {Y_choice:.3f}")
X_choice = choiceX(Fa=1779, Fr=Fr, Fa_C0_calc=Fa_C0_calc, e_calc=e_interp, df=df)
print(f"inter X2: {X_choice:.3f}")

def equivalent_radial_load(Fa, Fr, V, e, X, Y):
    if Fa / (V * Fr) <= e:
        return 0.47 * Fr
    else:
        return X*V*Fr + Y * Fa
    
def rotating_factor(type :str):
    if type == "inner":
        return 1
    elif type == "outer":
        return 1.2
# outer stationary so inner rotating 
Fe_calc = equivalent_radial_load(Fa, Fr, rotating_factor("inner"), e_interp, X_choice, Y_choice)
print(f"Equivalent radial load Fe: {Fe_calc:.2f} N")

