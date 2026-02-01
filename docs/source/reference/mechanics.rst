Mechanics
=========

.. list-table:: Analysis Comparison
   :widths: 20 40 40
   :header-rows: 1

   * - Feature
     - **Static Analysis (Beam)**
     - **Dynamics (RigidBody)**
   * - **Primary Goal**
     - Deformation & Stress
     - Motion & Forces
   * - **Key Variable**
     - $I$ (Inertia)
     - $m$ (Mass)
   * - **Governing Law**
     - Euler-Bernoulli Theory
     - Newton's Second Law ($F=ma$)
   * - **Main Output**
     - Deflection ($\delta$)
     - Acceleration ($a$)

---

Static Analysis
---------------

.. autoclass:: mechlab.mechanics.SimplySupportedBeam
  :members:
  :no-index:

.. autoclass:: mechlab.mechanics.Beam
   :members:
   :no-index:

.. autoclass:: mechlab.mechanics.StaticsParticle
  :members:
  :no-index:

Stress Analysis
---------------

.. autoclass:: mechlab.mechanics.StressState
  :members:
  :no-index:

.. autoclass:: mechlab.mechanics.StressTensor3D
  :members:
  :no-index:

.. autoclass:: mechlab.mechanics.StressTransform
  :members:
  :no-index:

.. autoclass:: mechlab.mechanics.PrincipalStresses
  :members:
  :no-index:

Rigid Body Dynamics
-------------------

.. autoclass:: mechlab.mechanics.RigidBody
   :members:
   :no-index:

.. autoclass:: mechlab.mechanics.DynamicsOfParticle
  :members:
  :no-index: