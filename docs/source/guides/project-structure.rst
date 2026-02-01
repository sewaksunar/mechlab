Project Structure
=================

This guide explains the MechLab module layout and how the codebase is organized
for a clean, modular workflow.

High-level layout
-----------------

.. code-block:: text

   mechlab/
   ├── mechanics/      → StressState, Beam, 3D tensors
   ├── units/          → SINGLE source for all unit handling
   ├── output/         → print_* and export_* functions
   ├── visual/         → GUI viewer, animations, Jupyter widgets
   ├── thermodynamics/ → State, properties
   ├── math/           → Basic formulas (stress, strain)
   ├── core/           → Base classes (re-exports units)
   ├── utils/          → is_jupyter() helper
   └── cli/            → Command-line interface

Module summary
--------------

- ``mechlab.mechanics`` – Stress analysis, beam calculations, statics, dynamics
- ``mechlab.units`` – Unit registry and conversion (single source of truth)
- ``mechlab.output`` – Text display (``print_stress``) and file export (``export_csv``, ``export_pdf``)
- ``mechlab.visual`` – Interactive plots (``StressViewer``), animations, Jupyter widgets
- ``mechlab.thermodynamics`` – Thermodynamic state and properties
- ``mechlab.math`` – Basic engineering formulas
- ``mechlab.core`` – Base classes, re-exports unit helpers for backward compatibility
- ``mechlab.cli`` – Command-line interface handlers

Design rules
------------

1. **Single source of truth**: Each concept lives in one place only
2. **No redundancy**: No duplicate code or overlapping modules
3. **Flat structure**: Minimal nesting, direct imports
4. **Lazy loading**: Optional dependencies don't block imports
5. **Backward compatible**: Old module names work with deprecation warnings

Stress workflow (example)
-------------------------

.. code-block:: python

   # Core stress logic
   from mechlab.mechanics import StressState
   state = StressState(100, 50, 25)

   # Output results
   from mechlab.output import print_stress, export_csv
   print_stress(state)
   export_csv(state.results(), 'results.csv')

   # Visualization
   from mechlab.visual import StressViewer
   StressViewer(100, 50, 25).show()

Deprecated modules
------------------

The following modules have been consolidated (old imports still work with warnings):

- ``mechlab.display`` → use ``mechlab.output``
- ``mechlab.export`` → use ``mechlab.output``
- ``mechlab.interactive`` → use ``mechlab.visual``
