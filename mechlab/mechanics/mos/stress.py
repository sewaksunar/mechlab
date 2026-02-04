"""DEFINITION OF STRESS AT A POINT"""
import sympy as sp
import numpy as np

class Stress:
    """Class representing normal stress components at a point.

    The constructor supports two calling styles:
    - Forces/areas: (F_xx, F_yy, F_zz, A_xx, A_yy, A_zz, F_xy, F_yz, F_zx, A_xy, A_yz, A_zx)
    - Direct stresses: (sigma_xx, sigma_yy, sigma_zz, tau_xy=0, tau_yz=0, tau_zx=0)
      When direct stresses are supplied, internal force/area fields are set with
      areas = 1.0 and forces = stresses.
    """

    def __init__(self, *args):
        # Forces + areas (12 args)
        if len(args) == 12:
            (F_xx, F_yy, F_zz, area_xx, area_yy, area_zz,
             F_xy, F_yz, F_zx, area_xy, area_yz, area_zx) = args
        # Direct stress components (6 args): sigma_xx, sigma_yy, sigma_zz, tau_xy, tau_yz, tau_zx
        elif len(args) == 6:
            sigma_xx, sigma_yy, sigma_zz, tau_xy, tau_yz, tau_zx = args
            # set areas to 1 and forces equal to stresses (so sigma = F/A)
            F_xx, F_yy, F_zz = float(sigma_xx), float(sigma_yy), float(sigma_zz)
            area_xx = area_yy = area_zz = 1.0
            F_xy, F_yz, F_zx = float(tau_xy), float(tau_yz), float(tau_zx)
            area_xy = area_yz = area_zx = 1.0
        # Only normal stresses provided (3 args)
        elif len(args) == 3:
            sigma_xx, sigma_yy, sigma_zz = args
            F_xx, F_yy, F_zz = float(sigma_xx), float(sigma_yy), float(sigma_zz)
            area_xx = area_yy = area_zz = 1.0
            F_xy = F_yz = F_zx = 0.0
            area_xy = area_yz = area_zx = 1.0
        else:
            raise TypeError("Stress requires either 3, 6, or 12 positional arguments")

        self.F_xx = F_xx
        self.F_yy = F_yy
        self.F_zz = F_zz
        self.area_xx = area_xx
        self.area_yy = area_yy
        self.area_zz = area_zz
        self.F_xy = F_xy
        self.F_yz = F_yz
        self.F_zx = F_zx
        self.area_xy = area_xy
        self.area_yz = area_yz
        self.area_zx = area_zx

    def normal_stress(self) -> np.ndarray:
        r"""Return normal stress components as a numpy array. 
        ..math: a = \lim_{delta A \to 0} \frac{\delta F_N}{\delta A}"""
        sigma_xx = self.F_xx / self.area_xx
        sigma_yy = self.F_yy / self.area_yy
        sigma_zz = self.F_zz / self.area_zz
        return np.array([sigma_xx, sigma_yy, sigma_zz])
    
    # def s_normal_stress(self) -> sp.Matrix:
    #     r"""Return symbolic normal stress components as a sympy Matrix.
    #     ..math: a = \lim_{delta A \to 0} \frac{\delta F_N}{\delta A}"""
    #     sigma_xx = sp.symbols('F_xx') / sp.symbols('A_xx')
    #     sigma_yy = sp.symbols('F_yy') / sp.symbols('A_yy')
    #     sigma_zz = sp.symbols('F_zz') / sp.symbols('A_zz')
    #     return sp.Matrix([sigma_xx, sigma_yy, sigma_zz])
    
    def shear_stress(self) -> np.ndarray:
        r"""Return shear stress components as a numpy array.
        ..math: a = \lim_{delta A \to 0} \frac{\delta F_S}{\delta A}"""
        tau_xy = self.F_xy / self.area_xy
        tau_yz = self.F_yz / self.area_yz
        tau_zx = self.F_zx / self.area_zx
        return np.array([tau_xy, tau_yz, tau_zx])

"""Full Stress Tensor at a Point"""
class StressTensor(Stress):
    """Class representing the full stress tensor at a point."""

    def stress_tensor(self) -> np.ndarray:
        r"""Return the full stress tensor as a 3x3 numpy array.

        Use the base-class (point-based) normal and shear stress calculations
        to avoid recursion when subclasses override plane-specific methods.
        """
        # Call the base-class implementations directly to avoid calling
        # overrides in subclasses (e.g., StressArbitraryPlane.normal_stress)
        sigma = Stress.normal_stress(self)
        tau = Stress.shear_stress(self)
        return np.array([[sigma[0], tau[0], tau[2]],
                         [tau[0], sigma[1], tau[1]],
                         [tau[2], tau[1], sigma[2]]])

    def traction_stress(self, nx, ny=None, nz=None) -> np.ndarray:
        r"""Compatibility method to compute traction/stress on a plane with normal ``n``.

        Accepts either a 3-element vector or three scalar components::

            traction_stress([nx, ny, nz])
            traction_stress(nx, ny, nz)

        Returns the traction vector T = sigma . n
        """
        # Build and normalize the normal vector from args
        if ny is None and nz is None:
            n = np.asarray(nx, dtype=float)
        else:
            n = np.array([nx, ny, nz], dtype=float)
        n = n / np.linalg.norm(n)
        return np.dot(self.stress_tensor(), n)

    # Backwards-compatible alias
    traction_vector = traction_stress

    def principal_stresses(self) -> np.ndarray:
        r"""Return principal stresses sorted in descending order."""
        vals = np.linalg.eigvalsh(self.stress_tensor())
        return np.sort(vals)[::-1]

    def principal_directions(self) -> np.ndarray:
        r"""Return principal direction unit vectors as columns ordered by descending principal stress."""
        vals, vecs = np.linalg.eigh(self.stress_tensor())
        order = np.argsort(vals)[::-1]
        return vecs[:, order]
    
"""Stresses Acting on Arbitrary Planes"""
class StressArbitraryPlane(StressTensor):
    """Class representing stress on an arbitrary plane defined by its normal vector.

    This class accepts the same constructor arguments as :class:`Stress` so it can be
    instantiated with stress/force components and areas. The plane normal can be
    supplied either during construction or when calling :meth:`traction_vector`.
    """

    def __init__(self, F_xx: float, F_yy: float, F_zz: float, area_xx: 
                    float, area_yy: float, area_zz: float,
                    F_xy=0, F_yz=0, F_zx=0, 
                    area_xy=1, area_yz=1, area_zx=1, 
                    normal_vector: np.ndarray = None):
        # Initialize stress components via parent
        super().__init__(F_xx, F_yy, F_zz, area_xx, area_yy, area_zz,
                            F_xy, F_yz, F_zx, area_xy, area_yz, area_zx)
        # Default normal is x-direction if not provided
        if normal_vector is None:
            self.normal_vector = np.array([1.0, 0.0, 0.0])
        else:
            self.normal_vector = np.asarray(normal_vector, dtype=float)
            self.normal_vector = self.normal_vector / np.linalg.norm(self.normal_vector)

    def traction_stress(self, nx, ny=None, nz=None) -> np.ndarray:
        r"""Return the traction vector on the plane defined by normal ``n``.

        Accepts either a 3-element vector or three scalar components::

            traction_stress([nx, ny, nz])
            traction_stress(nx, ny, nz)

        ..math: T = \sigma \cdot n
        """
        # Build and normalize the normal vector from args
        if ny is None and nz is None:
            n = np.asarray(nx, dtype=float)
        else:
            n = np.array([nx, ny, nz], dtype=float)
        n = n / np.linalg.norm(n)
        # Use the stress tensor method (do not overwrite the method with an attribute)
        return np.dot(self.stress_tensor(), n)
    
    """Normal and Shear Stress Components on the Arbitrary Plane"""
    def normal_stress(self) -> float:
        r"""Return the normal stress component on the arbitrary plane.

        ..math: \sigma_n = n \cdot (\sigma \cdot n)
        """
        n = self.normal_vector
        traction = np.dot(self.stress_tensor(), n)
        sigma_n = np.dot(n, traction)
        return sigma_n
    def shear_stress(self) -> np.ndarray:
        r"""Return the shear stress components on the arbitrary plane.

        ..math: \tau = T - \sigma_n n
        """
        n = self.normal_vector
        traction = np.dot(self.stress_tensor(), n)
        sigma_n = np.dot(n, traction)
        tau = traction - sigma_n * n
        return tau

class StressTransfomation:
    """Transformation of Stress under coordinate rotation.

    The stress tensor transforms according to: σ' = L σ L^T
    where L is the direction cosine matrix and σ is the stress tensor.

    This class supports two constructor styles:
    1. Provide a 3x3 stress tensor (and optional direction cosines matrix):
         StressTransfomation(sigma_matrix, direction_cosines)
    2. Provide component/area scalars and an optional rotation angle (degrees):
         StressTransfomation(F_xx, F_yy, F_zz, A_xx, A_yy, A_zz[, angle_deg])
       In the latter case a diagonal stress tensor is constructed from the
       normal stresses sigma = [F_xx/A_xx, F_yy/A_yy, F_zz/A_zz].
    """

    def __init__(self, *args, direction_cosines: np.ndarray = None):
        """Flexible initializer.

        Examples:
            StressTransfomation(sigma_matrix)
            StressTransfomation(sigma_matrix, direction_cosines=...)
            StressTransfomation(F_xx, F_yy, F_zz, A_xx, A_yy, A_zz)
            StressTransfomation(F_xx, F_yy, F_zz, A_xx, A_yy, A_zz, angle_deg)
        """
        # Initialize defaults
        self.L = direction_cosines if direction_cosines is not None else np.eye(3)
        self._angle_deg = None

        if len(args) == 0:
            raise TypeError("Provide either a stress tensor or component/area scalars")

        # Case 1: 3x3 stress tensor provided
        if len(args) == 1:
            sigma = np.asarray(args[0], dtype=float)
            if sigma.shape != (3, 3):
                raise ValueError("Provided stress tensor must be a 3x3 array")
            self.sigma = sigma
            return

        # Case 2: component/area scalars
        if len(args) >= 6:
            F_xx, F_yy, F_zz, A_xx, A_yy, A_zz = args[:6]
            self.sigma = np.diag([F_xx / A_xx, F_yy / A_yy, F_zz / A_zz])
            if len(args) >= 7:
                # Interpret 7th argument as rotation angle in degrees about z
                self._angle_deg = float(args[6])
            return

        raise TypeError("Invalid arguments to StressTransfomation initializer")

    def transform_stress(self, L: np.ndarray = None) -> np.ndarray:
        """Transform stress tensor: σ' = L σ L^T

        Args:
            L: Direction cosines matrix (3x3). Uses stored matrix if not provided.

        Returns:
            Transformed stress tensor as numpy array.
        """
        if L is None:
            L = self.L
        L = np.asarray(L, dtype=float)
        return np.dot(L, np.dot(self.sigma, L.T))

    def rotate_coordinates(self, angles: np.ndarray) -> np.ndarray:
        """Transform stress for rotation by Euler angles.

        Args:
            angles: Rotation angles [θx, θy, θz] in radians.

        Returns:
            Transformed stress tensor.
        """
        # Build rotation matrix from Euler angles
        Rx = self._rotation_matrix_x(angles[0])
        Ry = self._rotation_matrix_y(angles[1])
        Rz = self._rotation_matrix_z(angles[2])
        L = Rz @ Ry @ Rx
        return self.transform_stress(L)

    def transformed_stress(self) -> np.ndarray:
        """Return the transformed stress tensor using the provided angle (if any).

        If the instance was constructed with a single rotation angle (degrees),
        this performs a rotation about the z-axis by that angle. Otherwise returns
        the original stress tensor (or uses the stored direction cosines matrix).
        """
        if self._angle_deg is None:
            return self.sigma
        theta = np.deg2rad(self._angle_deg)
        L = self._rotation_matrix_z(theta)
        return self.transform_stress(L)

    @staticmethod
    def _rotation_matrix_x(theta):
        c, s = np.cos(theta), np.sin(theta)
        return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])

    @staticmethod
    def _rotation_matrix_y(theta):
        c, s = np.cos(theta), np.sin(theta)
        return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])

    @staticmethod
    def _rotation_matrix_z(theta):
        c, s = np.cos(theta), np.sin(theta)
        return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])
    
    def principle_stresses(self) -> np.ndarray:
        r"""Compute the principal stresses (eigenvalues of the stress tensor).

        Returns:
            Numpy array of principal stresses sorted in descending order.
        """
        sigma_transformed = self.transformed_stress()
        principal_stresses = np.linalg.eigvalsh(sigma_transformed)
        return np.sort(principal_stresses)[::-1]
    
    def stress_invariants(self) -> np.ndarray:
        r"""Compute the stress invariants I1, I2, I3.

        Returns:
            Numpy array of stress invariants [I1, I2, I3].
        """
        sigma_transformed = self.transformed_stress()
        I1 = np.trace(sigma_transformed)
        I2 = 0.5 * (I1**2 - np.trace(np.dot(sigma_transformed, sigma_transformed)))
        I3 = np.linalg.det(sigma_transformed)
        return np.array([I1, I2, I3])
    
    def max_shear_stress(self) -> float:
        r"""Compute the maximum shear stress.

        ..math: \tau_{max} = \frac{\sigma_1 - \sigma_3}{2}

        Returns:
            Maximum shear stress value.
        """
        principal_stresses = self.principle_stresses()
        tau_max = (principal_stresses[0] - principal_stresses[2]) / 2.0
        return tau_max
    
