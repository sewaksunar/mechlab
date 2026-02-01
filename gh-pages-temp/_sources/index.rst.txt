========
MechLab
========

.. raw:: html

   <div class="hero-section">
     <h1>A Modular Mechanical Engineering Laboratory for Python</h1>
     <p class="hero-description">
       MechLab is an open-source Python library for <strong>symbolic and numerical mechanical
       engineering computation</strong>. It provides a clean, engineering-focused API for stress analysis,
       unit conversions, thermodynamics, and interactive visualizations.
     </p>
     <div class="hero-features">
       <span class="feature-tag">mechanics</span> ·
       <span class="feature-tag">thermodynamics</span> ·
       <span class="feature-tag">units</span> ·
       <span class="feature-tag">visualization</span> ·
       <span class="feature-tag">output</span> ·
       <span class="feature-tag">cli</span>
     </div>
   </div>

.. code-block:: python
   :caption: Quick Example

   from mechlab.mechanics import StressState
   from mechlab.units import convert
   
   # Stress analysis
   state = StressState(100, 50, 25, unit="MPa")
   s1, s2 = state.principal()
   print(f"Principal stresses: {s1:.2f}, {s2:.2f} MPa")
   
   # Unit conversion
   psi = convert(100, 'MPa', 'psi')
   print(f"100 MPa = {psi:.0f} psi")

..

Getting Started
---------------

.. toctree::
   :maxdepth: 1

   installation/index
   tutorials/index
   examples/index

---

Learning & Reference
---------------------

.. toctree::
   :maxdepth: 2

   guides/index
   reference/index

---

Contribute & Explore
--------------------

.. toctree::
   :maxdepth: 1

   contributing/index
   faq/index
   changelog/index
