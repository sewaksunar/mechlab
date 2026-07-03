"""
Numerical/computation layer. Solvers know nothing about "beams" —
they operate on generic loads/supports handed to them. This keeps
domain classes decoupled from solving algorithms (Strategy pattern).
"""

from __future__ import annotations

import numpy as np

from mechlab.domain.entities import Load, Support


class EquilibriumSolver:
    """
    Solves reactions for a simply-supported system with exactly two
    vertical supports (pin/roller) under vertical loads only.
    """

    def solve_two_support_reactions(
        self, length: float, loads: list[Load], supports: list[Support]
    ) -> None:
        if len(supports) != 2:
            raise ValueError("This solver requires exactly 2 supports")

        s1, s2 = sorted(supports, key=lambda s: s.position)
        total_load = sum(load.total_force() for load in loads)
        total_moment_about_s1 = sum(load.moment_about(s1.position) for load in loads)

        span = s2.position - s1.position
        if span <= 0:
            raise ValueError("Supports must be at distinct, ordered positions")

        # Sum of moments about s1 = 0  =>  R2 * span = total_moment_about_s1
        s2.reaction_force = total_moment_about_s1 / span
        # Sum of vertical forces = 0
        s1.reaction_force = total_load - s2.reaction_force

class MatrixBeamSolver:
    """
    A general beam solver capable of solving statically determinate and
    indeterminate beams with any number of vertical supports using the
    Matrix Stiffness Method.
    """

    def solve(
        self,
        length: float,
        loads: list,
        supports: list,
        E: float = 2.0e11,  # Default Young's Modulus (Pascal)
        I_val: float = 1.0e-5  # Default Moment of Inertia (m^4)
    ) -> None:
        if not supports:
            raise ValueError("The structure must have at least one support to be stable.")

        # 1. Discretization: Find all unique coordinate points (Nodes)
        # Include boundary points, support locations, and load locations
        boundary_positions = {0.0, length}
        support_positions = {s.position for s in supports}
        load_positions = {load.position for load in loads}
        unique_positions = sorted(list(
            boundary_positions | support_positions | load_positions
        ))

        num_nodes = len(unique_positions)
        num_dofs = 2 * num_nodes  # 2 DOFs per node: [vertical displacement, rotation]

        # Map positions to node indices
        node_map = {pos: idx for idx, pos in enumerate(unique_positions)}

        # 2. Initialize Global Stiffness Matrix (K) and Force Vector (F)
        K_global = np.zeros((num_dofs, num_dofs))
        F_global = np.zeros(num_dofs)

        # 3. Assemble Global Stiffness Matrix
        for i in range(num_nodes - 1):
            x1 = unique_positions[i]
            x2 = unique_positions[i + 1]
            L = x2 - x1

            # Local stiffness matrix for a 2D Euler-Bernoulli beam element
            EI_L3 = (E * I_val) / (L ** 3)
            k_local = EI_L3 * np.array([
                [12,      6 * L,     -12,     6 * L],
                [6 * L,   4 * L ** 2, -6 * L,  2 * L ** 2],
                [-12,     -6 * L,    12,      -6 * L],
                [6 * L,   2 * L ** 2, -6 * L,  4 * L ** 2]
            ])

            # Global DOF indices for this element
            dofs = [2 * i, 2 * i + 1, 2 * (i + 1), 2 * (i + 1) + 1]

            # Mesh into global matrix
            for row_local, row_global in enumerate(dofs):
                for col_local, col_global in enumerate(dofs):
                    K_global[row_global, col_global] += k_local[row_local, col_local]

        # 4. Assemble External Forces
        # Assuming load.total_force() returns a positive magnitude acting downwards
        for load in loads:
            node_idx = node_map[load.position]
            F_global[2 * node_idx] -= load.total_force()

        # Keep copies for reaction recovery calculations later
        K_full = K_global.copy()
        F_full = F_global.copy()

        # 5. Apply Boundary Conditions (Restraints)
        restrained_dofs = []
        for support in supports:
            node_idx = node_map[support.position]
            v_dof = 2 * node_idx  # Restraining vertical displacement
            restrained_dofs.append(v_dof)

        # Penalty or Row-Zeroing method to enforce boundary conditions
        for dof in restrained_dofs:
            K_global[dof, :] = 0
            K_global[:, dof] = 0
            K_global[dof, dof] = 1.0
            F_global[dof] = 0.0

        # 6. Solve for Displacements
        try:
            displacements = np.linalg.solve(K_global, F_global)
        except np.linalg.LinAlgError as exc:
            raise ValueError("The system matrix is singular. Check if your beam is "
        "kinematically unstable.") from exc

        # 7. Recover Reaction Forces
        # R = K_full * u - F_full
        reactions = np.dot(K_full, displacements) - F_full

        # Map solved vertical reaction forces back to your Support objects
        for support in supports:
            node_idx = node_map[support.position]
            v_dof = 2 * node_idx
            # Rounding safely deals with minor floating-point noise
            support.reaction_force = round(reactions[v_dof], 4)
