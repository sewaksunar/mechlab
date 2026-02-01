Installation
============

MechLab requires Python 3.8+ and can be installed via pip.

Prerequisites
-------------

* **Python:** 3.8 or higher
* **Operating System:** Windows, macOS, or Linux

Installation Methods
--------------------

Choose the method that best fits your workflow.

.. tab-set::

   .. tab-item:: 📦 Pip (Recommended)
      :sync: pip

      Ideal for most users and environments.

      .. code-block:: bash

         pip install mechlab

   .. tab-item:: 🏗️ From Source
      :sync: source

      Best for contributors or those needing the latest features.

      .. code-block:: bash

         git clone https://github.com/sewaksunar/mechlab.git
         cd mechlab
         pip install -e .
         cd mechlab


Dependencies
------------

**Core dependencies** (automatically installed):

- ``numpy`` - Numerical computations
- ``rich`` - Terminal output formatting
- ``matplotlib`` - Plotting and visualization

**Optional dependencies** (for specific features):

.. code-block:: bash

   # For PDF export
   pip install reportlab

   # For Jupyter widgets
   pip install ipywidgets

Verify Installation
-------------------

Test your installation:

.. code-block:: bash

   # CLI check
   mechlab --version
   mechlab doctor

   # Python check
   python -c "import mechlab; print(f'MechLab {mechlab.__version__} successfully initialized.')"

.. tip::

   **Stuck?** If you encounter issues, try using a fresh virtual environment:
   
   .. code-block:: bash
   
      python -m venv mechlab_env
      # Windows: mechlab_env\\Scripts\\activate
      # Linux/Mac: source mechlab_env/bin/activate
      pip install mechlab
