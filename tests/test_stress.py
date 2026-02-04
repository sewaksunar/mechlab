import numpy as np
from mechlab.mechanics.mos.stress import StressTensor, StressArbitraryPlane


def make_sample():
    return StressTensor(1000, 1500, 2000, 10, 15, 20, 300, 400, 500, 5, 6, 7)


def test_stress_tensor_values():
    s = make_sample()
    expected = np.array([
        [100.0, 60.0, 71.42857143],
        [60.0, 100.0, 66.66666667],
        [71.42857143, 66.66666667, 100.0],
    ])
    assert s.stress_tensor().shape == (3, 3)
    assert np.allclose(s.stress_tensor(), expected, rtol=1e-7, atol=1e-9)


def test_traction_methods_equivalent():
    s = make_sample()
    n = np.array([1.0, 1.0, 1.0])
    n = n / np.linalg.norm(n)
    expected = np.dot(s.stress_tensor(), n)
    assert np.allclose(s.traction_stress(n), expected)
    assert np.allclose(s.traction_vector(n), expected)
    assert np.allclose(s.traction_stress(1, 1, 1), expected)


def test_stress_arbitrary_plane():
    s = make_sample()
    sap = StressArbitraryPlane(1000, 1500, 2000, 10, 15, 20, 300, 400, 500, 5, 6, 7, normal_vector=[1, 1, 1])
    assert np.allclose(sap.stress_tensor(), s.stress_tensor())
    assert np.allclose(sap.traction_vector([1, 1, 1]), np.dot(s.stress_tensor(), np.array([1.0, 1.0, 1.0]) / np.linalg.norm([1, 1, 1])))


def test_construct_with_direct_stresses():
    s = StressTensor(10, 30, 15, 0, 0, 0)
    # Principal stresses should be 30, 15, 10
    p = s.principal_stresses()
    assert np.allclose(p, np.array([30.0, 15.0, 10.0]))
    # Principal directions should satisfy sigma v = lambda v
    dirs = s.principal_directions()
    for i in range(3):
        assert np.allclose(np.dot(s.stress_tensor(), dirs[:, i]), p[i] * dirs[:, i])


def test_construct_with_three_normals():
    s = StressTensor(100.0, 50.0, 25.0)
    p = s.principal_stresses()
    assert np.allclose(p, np.sort(np.array([100.0, 50.0, 25.0]))[::-1])


def test_principal_directions_for_oblique_case():
    # σxx=10, σyy=30, σzz=15, σxy=7.5 => principal stresses [32.5, 15, 7.5]
    s = StressTensor(10, 30, 15, 7.5, 0, 0)
    p = s.principal_stresses()
    assert np.allclose(p, np.array([32.5, 15.0, 7.5]))
    pd = s.principal_directions()
    expected = np.array([
        [0.31622777, 0.0, -0.9486833],
        [0.9486833, 0.0, 0.31622777],
        [0.0, 1.0, 0.0]
    ])
    # Each principal direction matches expected up to sign
    for i in range(3):
        v = pd[:, i]
        exp = expected[:, i]
        assert np.allclose(v, exp, atol=1e-6) or np.allclose(v, -exp, atol=1e-6)
