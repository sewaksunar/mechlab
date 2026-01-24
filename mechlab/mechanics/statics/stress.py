'''
Theory of Stress
'''

class StressTensor3D:
    def __init__(self, components):
        """
        Initialize a 3D stress tensor.

        Parameters:
        components (list of list of float): A 3x3 matrix representing the stress tensor.
        """
        if len(components) != 3 or any(len(row) != 3 for row in components):
            raise ValueError("Stress tensor must be a 3x3 matrix.")
        self.components = components

    def get_components(self):
        """
        Get the components of the stress tensor.

        Returns:
        list of list of float: The 3x3 matrix representing the stress tensor.
        """
        return self.components

class StressOnArbitaryPlane:
    @staticmethod
    def calculate_stress(stress_tensor, normal_vector):
        """
        Calculate the stress on an arbitrary plane given the stress tensor and the normal vector.

        Parameters:
        stress_tensor (list of list of float): A 3x3 matrix representing the stress tensor.
        normal_vector (list of float): A 3-element list representing the normal vector of the plane.

        Returns:
        list of float: The stress vector on the plane.

        Example:
        --------
        stress_tensor = [
            [100, 30, 20],
            [30, 80, 10],
            [20, 10, 60]
        ]
        normal_vector = [1, 0, 0]
        stress_on_plane = StressOnArbitaryPlane.calculate_stress(stress_tensor, normal_vector)
        print(stress_on_plane)  # Output: [100, 30, 20]
        """
        import numpy as np

        # Convert inputs to numpy arrays for easier calculations
        stress_matrix = np.array(stress_tensor)
        normal_vec = np.array(normal_vector)

        # Calculate the stress vector on the plane
        stress_on_plane = np.dot(stress_matrix, normal_vec)

        return stress_on_plane.tolist()


class StressTransformations3D:
    @staticmethod
    def principal_stresses(stress_tensor, direction_cosines):
        """
        Calculate the principal stresses from a given stress tensor.

        Parameters:
        stress_tensor (list of list of float): A 3x3 matrix representing the stress tensor.
        direction_cosines (list of float): A list of direction cosines for the transformation.

        Returns:
        list of float: The principal stresses sorted in descending order.


        """
        import numpy as np

        # Convert inputs to numpy arrays for easier calculations
        stress_matrix = np.array(stress_tensor)
        
        # direction cosines matrix for transformation4

# stress_transform.py
import sympy as sp

class StressTransform:
    '''
    Class to perform symbolic stress tensor transformations in 3D.
    The transformation is defined by direction cosines between two coordinate systems.
    1. Define direction cosines l1, m1, n1; l2, m2, n2; l3, m3, n3
    2. Define stress tensor components sxx, syy, szz, sxy, syz, sxz
    3. Compute transformed stress tensor using σ' = L * σ * L.T
    4. Extract transformed components sXX, sYY, sZZ
    5. Provide method to evaluate numerically given specific values

    usage:
    st = StressTransform()
    components = st.components()
    print(components["sXX"])
    values = { st.sxx: 100, st.syy: 50, st.szz: 75,
               st.sxy: 20,  st.syz: 15, st.sxz: 10,
                st.l1: 1, st.m1: 0, st.n1: 0,
                st.l2: 0, st.m2: 1, st.n2: 0,
                st.l3: 0, st.m3: 0, st.n3: 1 }
    tensor_XYZ = st.evaluate(values)
    print(tensor_XYZ)
    '''
    def __init__(self):
        # Define symbols for direction cosines
        self.l1, self.m1, self.n1 = sp.symbols('l1 m1 n1')
        self.l2, self.m2, self.n2 = sp.symbols('l2 m2 n2')
        self.l3, self.m3, self.n3 = sp.symbols('l3 m3 n3')

        # Define symbols for stress tensor components
        self.sxx, self.syy, self.szz = sp.symbols('sxx syy szz')
        self.sxy, self.syz, self.sxz = sp.symbols('sxy syz sxz')

        # Direction cosine matrix
        self.direction_cosines = sp.Matrix([
            [self.l1, self.m1, self.n1],
            [self.l2, self.m2, self.n2],
            [self.l3, self.m3, self.n3]
        ])

        # Stress tensor in original coordinates
        self.stress_tensor_xyz = sp.Matrix([
            [self.sxx, self.sxy, self.sxz],
            [self.sxy, self.syy, self.syz],
            [self.sxz, self.syz, self.szz]
        ])

    def transform(self):
        """Symbolic stress tensor transformation: σ' = L * σ * L.T"""
        return self.direction_cosines * self.stress_tensor_xyz * self.direction_cosines.T

    def components(self):
        """Return simplified symbolic transformed components sXX, sYY, sZZ"""
        stress_tensor_XYZ = self.transform()
        return {
            "sXX": sp.simplify(stress_tensor_XYZ[0, 0]),
            "sYY": sp.simplify(stress_tensor_XYZ[1, 1]),
            "sZZ": sp.simplify(stress_tensor_XYZ[2, 2])
        }

    def evaluate(self, values):
        """
        Evaluate the transformed tensor numerically.
        :param values: dict mapping symbols to numerical values
        :return: evaluated stress tensor (sympy Matrix with numbers)
        """
        stress_tensor_XYZ = self.transform()
        return stress_tensor_XYZ.evalf(subs=values)

class PrincipalStresses:
    @staticmethod
    def calculate(stress_tensor):
        """
        Calculate the principal stresses from a given stress tensor.

        Parameters:
        stress_tensor (list of list of float): A 3x3 matrix representing the stress tensor.

        Returns:
        list of float: The principal stresses sorted in descending order.
        """
        import numpy as np

        # Convert input to numpy array
        stress_matrix = np.array(stress_tensor)

        # Calculate eigenvalues (principal stresses)
        principal_stresses = np.linalg.eigvalsh(stress_matrix)

        # Sort in descending order
        principal_stresses_sorted = np.sort(principal_stresses)[::-1]

        # orientation of principal stresses
        

        return principal_stresses_sorted.tolist()

import matplotlib.pyplot as plt
class MohorCircle:
    @staticmethod
    def calculate(stress_tensor, normal_vector):
        """
        Calculate the stress on an arbitrary plane given the stress tensor and the normal vector.

        Parameters:
        stress_tensor (list of list of float): A 3x3 matrix representing the stress tensor.
        normal_vector (list of float): A 3-element list representing the normal vector of the plane.

        Returns:
        list of float: The stress vector on the plane.
        """
        import numpy as np

        # Convert inputs to numpy arrays for easier calculations
        stress_matrix = np.array(stress_tensor)
        normal_vec = np.array(normal_vector)

        # Calculate the stress vector on the plane
        stress_on_plane = np.dot(stress_matrix, normal_vec)

        return stress_on_plane.tolist()