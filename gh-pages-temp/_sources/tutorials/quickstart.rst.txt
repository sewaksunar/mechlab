Quickstart
==========

This guide will get you up and running with **MechLab** in under 5 minutes.

Installation
------------

.. code-block:: bash

   pip install mechlab

1. Stress Analysis
------------------

The most common use case - plane stress analysis:

.. code-block:: python

   from mechlab.mechanics import StressState

   # Create stress state (σx=100, σy=50, τxy=25 MPa)
   state = StressState(100, 50, 25, unit="MPa")

   # Get principal stresses
   s1, s2 = state.principal()
   print(f"Principal stresses: σ1={s1:.2f}, σ2={s2:.2f} MPa")

   # Get all results
   results = state.results()
   print(f"Von Mises stress: {results['von_mises']:.2f} MPa")

2. Unit Conversion
------------------

Convert between engineering units:

.. code-block:: python

   from mechlab.units import convert

   # Convert 100 MPa to psi
   psi_value = convert(100, 'MPa', 'psi')
   print(f"100 MPa = {psi_value:.2f} psi")

   # Convert 1 meter to feet
   feet = convert(1, 'm', 'ft')
   print(f"1 m = {feet:.4f} ft")

3. Output & Export
------------------

Display results and export to files:

.. code-block:: python

   from mechlab.mechanics import StressState
   from mechlab.output import print_stress, export_csv

   state = StressState(100, 50, 25)

   # Print formatted results
   print_stress(state)

   # Export to CSV
   export_csv(state.results(), 'stress_results.csv')

4. Visualization
----------------

Interactive Mohr's circle:

.. code-block:: python

   from mechlab.visual import StressViewer

   # Launch interactive viewer
   viewer = StressViewer(100, 50, 25)
   viewer.show()

5. Command-Line Interface
-------------------------

MechLab also provides a CLI:

.. code-block:: bash

   # Stress analysis
   mechlab stress compute --sx 100 --sy 50 --txy 25

   # Unit conversion
   mechlab units convert 100 MPa psi

   # Check installation
   mechlab doctor

Next Steps
----------

* Explore the :doc:`../reference/index` for full API documentation
* See :doc:`../examples/index` for complete code examples
* Read the :doc:`../guides/project-structure` to understand the module layout