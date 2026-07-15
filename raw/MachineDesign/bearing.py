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
print(f"Interpolated X2: {X_choice:.3f}")

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

# Table 11–2 Dimensions and Load Ratings for Single-Row 02-Series Deep-Groove and Angular-Contact Ball Bearings (data is structured using a hierarchical MultiIndex to categorise)
columns = pd.MultiIndex.from_tuples([
    ('Dimensions', 'Bore (mm)'),
    ('Dimensions', 'OD (mm)'),
    ('Dimensions', 'Width (mm)'),
    ('Dimensions', 'Fillet (mm)'),

    ('Shoulder Dia', 'dS (mm)'),
    ('Shoulder Dia', 'dH (mm)'),

    ('Deep-Groove', 'C10 (kN)'),
    ('Deep-Groove', 'C0 (kN)'),

    ('Angular-Contact', 'C10 (kN)'),
    ('Angular-Contact', 'C0 (kN)')
])

# Data extracted from Source 3 [2]
data = [
    [10, 30,  9, 0.6, 12.5,  27,  5.07, 2.24,  4.94, 2.12],
    [12, 32, 10, 0.6, 14.5,  28,  6.89, 3.10,  7.02, 3.05],
    [15, 35, 11, 0.6, 17.5,  31,  7.80, 3.55,  8.06, 3.65],
    [17, 40, 12, 0.6, 19.5,  34,  9.56, 4.50,  9.95, 4.75],
    [20, 47, 14, 1.0, 25.0,  41, 12.7,  6.20, 13.3,  6.55],
    [25, 52, 15, 1.0, 30.0,  47, 14.0,  6.95, 14.8,  7.65],
    [30, 62, 16, 1.0, 35.0,  55, 19.5, 10.0,  20.3, 11.0],
    [35, 72, 17, 1.0, 41.0,  65, 25.5, 13.7,  27.0, 15.0],
    [40, 80, 18, 1.0, 46.0,  72, 30.7, 16.6,  31.9, 18.6],
    [45, 85, 19, 1.0, 52.0,  77, 33.2, 18.6,  35.8, 21.2],
    [50, 90, 20, 1.0, 56.0,  82, 35.1, 19.6,  37.7, 22.8],
    [55, 100, 21, 1.5, 63.0,  90, 43.6, 25.0,  46.2, 28.5],
    [60, 110, 22, 1.5, 70.0,  99, 47.5, 28.0,  55.9, 35.5],
    [65, 120, 23, 1.5, 74.0, 109, 55.9, 34.0,  63.7, 41.5],
    [70, 125, 24, 1.5, 79.0, 114, 61.8, 37.5,  68.9, 45.5],
    [75, 130, 25, 1.5, 86.0, 119, 66.3, 40.5,  71.5, 49.0],
    [80, 140, 26, 2.0, 93.0, 127, 70.2, 45.0,  80.6, 55.0],
    [85, 150, 28, 2.0, 99.0, 136, 83.2, 53.0,  90.4, 63.0],
    [90, 160, 30, 2.0, 104.0, 146, 95.6, 62.0, 106.0, 73.5],
    [95, 170, 32, 2.0, 110.0, 156, 108.0, 69.5, 121.0, 85.0]
]

# Create the DataFrame
df_02_series_bearings = pd.DataFrame(data, columns=columns)
print(df_02_series_bearings)


# problem 11-25
# desing parameters and life claculation 
Fr = 8000  # radial load in N
Fa = 2000  # axial load in N
# desin life in hours
hLD = 10000 # desing life in hours
nD = 400 # speed in rev/min
V = 1 # rotation factor (as inner ring is rotaing)
af = 1 # application factor (assumeing normal operating conditions)

# weibull parameters for bearing life calculation 
# menufactureer 2 (with rating life of 10^6 revs)
L10 = 10**6 # rating life in revs
x0 = 0.02
theta = 4.439
b = 1.483
RD = 0.99

# calcuation of xD

def xD(LD, L10):
    return (LD / L10)

def hL2L(hLD, nD):
    return 60*hLD*nD

xD_calc = xD(hL2L(hLD, nD), L10)
print(f"xD = {xD_calc:.3f} L10")

# estimation of catalog load rating C10 based on the given loads and life

# equivalent radial load Fe
# assuming 
e = 0.27 
FaVFr = Fa/(V*Fr)
print(f"Fa/(V*Fr) = {FaVFr:.3f}")

row_values = df.loc[df[('e', '')] == e].iloc[0].values
X = row_values[2]  # X2 value
Y = row_values[4]  # Y2 value
print(f"X = {X}, Y = {Y}")

Fe_calc = equivalent_radial_load(Fa, Fr, V, e, X, Y)
print(f"Equivalent radial load Fe = {Fe_calc:.2f} N")

Fe_calc = 7.74*10e3 # N (assume)
def C10(af, FD, xD, x0, theta, RD, a, b):
    den = x0 + (theta - x0) * (np.log(1/RD))**(1/b)
    return af * FD * (xD/den)**(1/a)
FD = 8000
c10_calc = C10(af, FD, xD_calc, x0, theta, 0.9, 3, b)
print(f"Estimated C10 = {c10_calc:.2f} N")


