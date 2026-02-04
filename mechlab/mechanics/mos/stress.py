"""DEFINITION OF STRESS AT A POINT"""
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

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

    def mohr_circle(self, plane: str = 'xy') -> dict:
        r"""Compute Mohr's circle parameters for a given in-plane stress (2D).

        Args:
            plane: one of 'xy', 'yz', or 'zx' indicating which plane to use.

        Returns:
            dict with keys: 'center', 'radius', 'sigma1', 'sigma2', 'angle_rad',
            'sigma_x', 'sigma_y', 'tau_xy'
        """
        if plane == 'xy':
            sigma_x = self.stress_tensor()[0, 0]
            sigma_y = self.stress_tensor()[1, 1]
            tau = self.stress_tensor()[0, 1]
        elif plane == 'yz':
            sigma_x = self.stress_tensor()[1, 1]
            sigma_y = self.stress_tensor()[2, 2]
            tau = self.stress_tensor()[1, 2]
        elif plane == 'zx' or plane == 'xz':
            sigma_x = self.stress_tensor()[2, 2]
            sigma_y = self.stress_tensor()[0, 0]
            tau = self.stress_tensor()[2, 0]
        else:
            raise ValueError("plane must be one of 'xy', 'yz', 'zx'")

        center = 0.5 * (sigma_x + sigma_y)
        radius = np.sqrt(((sigma_x - sigma_y) / 2.0) ** 2 + tau ** 2)
        sigma1 = center + radius
        sigma2 = center - radius
        angle_rad = 0.5 * np.arctan2(2.0 * tau, (sigma_x - sigma_y))
        return {
            'center': center,
            'radius': radius,
            'sigma1': sigma1,
            'sigma2': sigma2,
            'angle_rad': angle_rad,
            'sigma_x': sigma_x,
            'sigma_y': sigma_y,
            'tau_xy': tau,
        }

    def mohr_circle_points(self, plane: str = 'xy', n_points: int = 128) -> tuple[np.ndarray, np.ndarray]:
        """Return arrays (sigma_vals, tau_vals) for plotting Mohr's circle."""
        params = self.mohr_circle(plane)
        theta = np.linspace(0, 2 * np.pi, n_points)
        sigma_vals = params['center'] + params['radius'] * np.cos(theta)
        tau_vals = params['radius'] * np.sin(theta)
        return sigma_vals, tau_vals

    def plot_mohr_circle(self, plane: str = 'xy', ax=None, show: bool = True) -> 'matplotlib.axes.Axes':
        """Plot Mohr's circle for the specified plane.

        Requires matplotlib to be installed. Returns the Axes object.
        """
        import matplotlib.pyplot as plt

        sigma_vals, tau_vals = self.mohr_circle_points(plane)
        params = self.mohr_circle(plane)

        if ax is None:
            fig, ax = plt.subplots()
        ax.plot(sigma_vals, tau_vals, label="Mohr's circle")
        ax.axhline(0, color='k', linewidth=0.5)
        # Mark principal stresses
        ax.plot([params['sigma1'], params['sigma2']], [0, 0], 'ro', label='Principal stresses')
        # Mark original stress points
        ax.plot([params['sigma_x']], [params['tau_xy']], 'bx', label=f"(σx, τ)={params['sigma_x'], params['tau_xy']}")
        ax.plot([params['sigma_y']], [-params['tau_xy']], 'gx', label=f"(σy, -τ)={params['sigma_y'], -params['tau_xy']}")
        ax.set_xlabel('Normal stress (σ)')
        ax.set_ylabel('Shear stress (τ)')
        ax.set_aspect('equal', 'box')
        ax.legend()
        if show:
            plt.show()
        return ax

    def save_mohr_circle(self, filename: str, plane: str = 'xy', dpi: int = 150) -> None:
        """Save Mohr's circle plot to a file.

        Args:
            filename: Path to save the figure (supports formats matplotlib accepts).
            plane: Plane to use ('xy', 'yz', 'zx').
            dpi: Dots per inch for saved figure.
        """
        import matplotlib.pyplot as plt
        ax = self.plot_mohr_circle(plane=plane, ax=None, show=False)
        fig = ax.get_figure()
        fig.savefig(filename, dpi=dpi, bbox_inches='tight')
        plt.close(fig)

    def plot_principal_mohr(self, ax=None, show: bool = True, filename: str | None = None) -> 'matplotlib.axes.Axes':
        """Plot the three principal Mohr circles (σ1-σ2, σ2-σ3, σ3-σ1).

        Args:
            ax: Optional matplotlib Axes to draw on.
            show: If True, display the figure with plt.show().
            filename: If provided, save the figure to this path and do not show.

        Returns:
            The matplotlib Axes containing the plot.
        """
        import matplotlib
        import matplotlib.pyplot as plt

        # Use a non-interactive backend when saving to file or when running in headless
        if filename is not None:
            matplotlib.use('Agg')

        prin = self.principal_stresses()
        pairs = [ (0,1), (1,2), (2,0) ]

        if ax is None:
            fig, ax = plt.subplots(figsize=(6,6))
        colors = ['C0','C1','C2']
        max_sigma = np.max(prin)
        min_sigma = np.min(prin)
        all_centers = []
        all_radii = []
        for (a,b), c in zip(pairs, colors):
            center = 0.5*(prin[a]+prin[b])
            radius = abs(prin[a]-prin[b])/2.0
            theta = np.linspace(0, 2*np.pi, 400)
            sigma_vals = center + radius * np.cos(theta)
            tau_vals = radius * np.sin(theta)
            ax.plot(sigma_vals, tau_vals, color=c, label=f'σ{a+1}-σ{b+1}')
            ax.plot([prin[a], prin[b]], [0,0], 'o', color=c)
            all_centers.append(center)
            all_radii.append(radius)
        ax.set_xlabel('Normal stress (σ)')
        ax.set_ylabel('Shear stress (τ)')
        ax.set_aspect('equal', 'box')
        ax.legend()
        # Set limits to include all circles with some margin
        left = min(all_centers[i]-all_radii[i] for i in range(len(all_centers)))
        right = max(all_centers[i]+all_radii[i] for i in range(len(all_centers)))
        margin = 0.1*(right-left)
        ax.set_xlim(left-margin, right+margin)
        ax.set_ylim(- (max(all_radii)+margin), (max(all_radii)+margin))

        if filename is not None:
            fig = ax.get_figure()
            fig.savefig(filename, dpi=150, bbox_inches='tight')
            plt.close(fig)
            if show:
                print(f"Saved principal Mohr circles to: {filename}")
            return ax

        if show:
            plt.show()
        return ax

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
    
    def von_mises_stress(self) -> float:
        r"""Compute the von Mises stress.

        ..math: \sigma_v = \sqrt{\frac{1}{2}[(\sigma_1 - \sigma_2)^2 + (\sigma_2 - \sigma_3)^2 + (\sigma_3 - \sigma_1)^2]}

        Returns:
            Von Mises stress value.
        """
        principal_stresses = self.principle_stresses()
        s1, s2, s3 = principal_stresses
        von_mises = np.sqrt(0.5 * ((s1 - s2) ** 2 + (s2 - s3) ** 2 + (s3 - s1) ** 2))
        return von_mises
    
    def mohr_circle_parameters(self) -> dict:
        r"""Compute Mohr's circle parameters for 3D stress state.

        Returns:
            Dictionary containing:
                - 'center': Center of the Mohr's circle (σ_avg)
                - 'radius': Radius of the Mohr's circle (R)
                - 'principal_stresses': Principal stresses (σ1, σ2, σ3)
        """
        principal_stresses = self.principle_stresses()
        sigma_avg = np.mean(principal_stresses)
        radius = max(abs(principal_stresses - sigma_avg))
        return {
            'center': sigma_avg,
            'radius': radius,
            'principal_stresses': principal_stresses
        }
    def mohr_circle_plot(self, num_points=100) -> dict:
        r"""Generate points for Mohr's circle plot.

        Args:
            num_points: Number of points to generate on the circle.
        Returns:
            Dictionary with 'x' and 'y' arrays for the circle.
        """
        params = self.mohr_circle_parameters()
        center = params['center']
        radius = params['radius']
        theta = np.linspace(0, 2 * np.pi, num_points)
        x = center + radius * np.cos(theta)
        y = radius * np.sin(theta)
        return {'x': x, 'y': y, 'center': center, 'radius': radius}
    def plot_mohr_circle(self, ax=None, show=True, **kwargs):
        """
        Plot Mohr's circle for the current stress state.

        Args:
            ax: Optional matplotlib Axes object. If None, creates a new figure.
            show: If True, calls plt.show().
            **kwargs: Additional keyword arguments passed to plt.plot.

        Returns:
            The matplotlib Axes object containing the plot.
        """
        params = self.mohr_circle_parameters()
        circle = self.mohr_circle_plot()
        if ax is None:
            fig, ax = plt.subplots(figsize=(6, 6))
        ax.plot(circle['x'], circle['y'], label="Mohr's Circle", **kwargs)
        # Plot principal stresses on the horizontal axis
        for s in params['principal_stresses']:
            ax.plot([s], [0], 'ro')
            ax.annotate(f"{s:.2f}", (s, 0), textcoords="offset points", xytext=(0,10), ha='center')
        # Plot center
        ax.plot([params['center']], [0], 'bo', label='Center')
        ax.set_xlabel('Normal Stress (σ)')
        ax.set_ylabel('Shear Stress (τ)')
        ax.set_title("Mohr's Circle")
        ax.grid(True)
        ax.set_aspect('equal', 'box')
        ax.legend()
        if show:
            plt.show()
        return ax