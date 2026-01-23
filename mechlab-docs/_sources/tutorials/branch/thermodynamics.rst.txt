Thermodynamics
========================

.. # 1. Fetch the module discussion but EXCLUDE the class to prevent duplication
.. automodule:: mechlab.thermodynamics.state
   :no-index:
   :exclude-members: State

   .. rubric:: Core Class
   
   .. # 2. Manually fetch the class here so it sits under your custom rubric
   .. autoclass:: State
      :members:
      :special-members: __init__
      :exclude-members: _h, _s, _T, _P  # Hides internal implementation details
      :no-index: