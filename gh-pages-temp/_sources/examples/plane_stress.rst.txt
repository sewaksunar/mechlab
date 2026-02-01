Plane Stress Example
====================

This example demonstrates a plane stress calculation using ``StressState``.

Overview
--------

Plane stress analysis computes:

- Principal stresses (σ₁, σ₂)
- Maximum shear stress (τₘₐₓ)
- Von Mises equivalent stress

Code
----

.. literalinclude:: ../../../examples/plane_stress.py
   :language: python
   :linenos:

Running
-------

.. code-block:: bash

   python examples/plane_stress.py

   # Or via CLI:
   mechlab stress compute --sx 100 --sy 50 --txy 25

Output
------

.. code-block:: text

   Plane Stress Results
        σx = 100.000 MPa
        σy = 50.000 MPa
       τxy = 25.000 MPa
        σ1 = 110.355 MPa
        σ2 = 39.645 MPa
      τmax = 35.355 MPa
   von_mises = 96.825 MPa
