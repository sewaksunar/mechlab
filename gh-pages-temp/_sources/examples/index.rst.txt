Examples
========

Worked examples demonstrating real engineering workflows.

Each example shows how to apply MechLab's modules to practical problems,
combining symbolic and numerical computation with clear outputs.

.. toctree::
   :maxdepth: 2

   plane_stress
   stress_transform

Running Examples
----------------

All examples are available as scripts in the ``examples/`` folder:

.. code-block:: bash

   python examples/plane_stress.py
   python examples/stress_transform.py

Or use the CLI for quick calculations:

.. code-block:: bash

   mechlab stress compute --sx 100 --sy 50 --txy 25
   mechlab units convert 100 MPa psi
