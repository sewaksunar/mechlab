Quickstart
==========

This guide will get you up and running with **MechLab** for thermodynamic modeling in under 5 minutes.

Installation
------------
Ensure you have the library installed in your environment:

.. code-block:: bash

   pip install mechlab

I. Example
-------------------------
MechLab uses **SymPy** for symbolic relationships and **NumPy** for numerical evaluation. The core of the library is the Ideal Gas Law:

.. math::

   P \cdot V = n \cdot R \cdot T

Here is how to calculate the pressure of a system:

.. code-block:: python

   from mechlab.thermodynamics import state

   # Define system parameters
   moles = 1.0       # n
   gas_const = 8.314 # R (J/mol·K)
   temp = 300        # T (Kelvin)
   volume = 0.025    # V (m^3)

   # Get the pressure function
   p_func = state.get_pressure_func()
   pressure = p_func(moles, gas_const, temp, volume)

   print(f"The system pressure is: {pressure:.2f} Pa")

Next Steps
----------
* Explore the :doc:`../reference/index` for more advanced state functions.
* Check out the :doc:`../guides/index` for complex cycle modeling (Rankine, Otto, etc.).