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
     - Equilibrium & Weight
   * - **Key Variable**
     - $I$ (Inertia)
     - $m$ (Mass)
   * - **Governing Law**
     - Euler-Bernoulli Theory
     - Newton's Second Law ($F=ma$)
   * - **Main Output**
     - Deflection ($\delta$)
     - Weight ($W$)

---

Static Analysis
---------------

.. autoclass:: mechlab.mechanics.Beam
   :members:
   :no-index:



Rigid Body Dynamics
-------------------

.. autoclass:: mechlab.mechanics.RigidBody
   :members:
   :no-index: