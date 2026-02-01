Engineering Guides
==================

.. toctree::
   :maxdepth: 1

   project-structure

Best Practices for Units
------------------------

Always use the ``mechlab.units`` module for conversions:

.. code-block:: python

   from mechlab.units import convert, UNITS

   # Convert between units
   psi = convert(100, 'MPa', 'psi')

   # See all available units
   print(UNITS.keys())  # length, force, pressure, mass, area, moment

Integration with NumPy
----------------------

MechLab is designed to be array-compatible. You can pass NumPy arrays into most
Mechanics functions to analyze multiple load points simultaneously.

.. code-block:: python

   import numpy as np
   from mechlab.math import stress

   forces = np.array([100, 200, 300])  # N
   area = 0.01  # m²

   stresses = stress(forces, area)
   print(stresses)  # [10000. 20000. 30000.] Pa