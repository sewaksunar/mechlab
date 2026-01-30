"""3D stress transformation example (symbolic + numeric)."""

import sympy as sp

from mechlab.mechanics.statics.stress import StressTransform


def main() -> None:
    st = StressTransform()

    # Symbolic transform
    sigma_xyz = st.transform()
    print("Symbolic σ' = L σ Lᵀ:")
    print(sigma_xyz)

    # Numerical substitution
    values = {
        st.sxx: 100,
        st.syy: 50,
        st.szz: 75,
        st.sxy: 20,
        st.syz: 15,
        st.sxz: 10,
        st.l1: 1,
        st.m1: 0,
        st.n1: 0,
        st.l2: 0,
        st.m2: 1,
        st.n2: 0,
        st.l3: 0,
        st.m3: 0,
        st.n3: 1,
    }

    sigma_numeric = sp.Matrix(sigma_xyz).subs(values)
    print("\nNumerical Transformed Stress Tensor:")
    print(sigma_numeric)


if __name__ == "__main__":
    main()
