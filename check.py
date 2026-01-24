from mechlab.mechanics.statics.stress import StressOnArbitaryPlane, StressTransform

# Initialize
st = StressTransform()

# Define numerical values
values = {
    st.sxx: 100, st.syy: 50, st.szz: 75,
    st.sxy: 20,  st.syz: 15, st.sxz: 10,
    st.l1: 1, st.m1: 0, st.n1: 0,   # X aligned with x
    st.l2: 0, st.m2: 1, st.n2: 0,   # Y aligned with y
    st.l3: 0, st.m3: 0, st.n3: 1    # Z aligned with z
}

# Compute transformed tensor
tensor_XYZ = st.evaluate(values)
print("Numerical Transformed Stress Tensor:")
print(tensor_XYZ)

# Extract components
print("sXX =", tensor_XYZ[0, 0])
print("sYY =", tensor_XYZ[1, 1])
print("sZZ =", tensor_XYZ[2, 2])
