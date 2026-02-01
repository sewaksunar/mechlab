Stress Transform Example
========================

This example demonstrates a symbolic and numeric 3D stress transformation.

Overview
--------

The 3D stress transformation uses direction cosines to rotate the stress tensor:

.. math::

   \sigma' = L \cdot \sigma \cdot L^T

where *L* is the transformation matrix of direction cosines.

Code
----

.. literalinclude:: ../../../examples/stress_transform.py
   :language: python
   :linenos:

Running
-------

.. code-block:: bash

   python examples/stress_transform.py

Output
------

The script outputs both symbolic and numeric results:

1. **Symbolic**: General transformation formula with SymPy symbols
2. **Numeric**: Concrete values after substituting specific direction cosines
