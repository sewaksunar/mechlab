Installation
============

MechLab is designed to be lightweight and modular. We strongly recommend using a virtual environment (via Poetry or venv) to ensure your engineering dependencies remain isolated and stable.



Prerequisites
-------------

Before installing, ensure your system meets these requirements:

* **Python:** 3.9 or higher
* **Operating System:** Windows, macOS, or Linux
* **Core Libraries:** NumPy, SciPy (installed automatically)

Installation Methods
--------------------

Choose the method that best fits your workflow.

.. tab-set::

   .. tab-item:: 📦 Poetry (Recommended)
      :sync: poetry

      Use this for reproducible engineering projects. Poetry ensures your dependency tree is locked.

      .. code-block:: bash

         poetry add mechlab

   .. tab-item:: 🐍 Pip
      :sync: pip

      Ideal for simple scripts, Jupyter Notebooks, or Google Colab environments.

      .. code-block:: bash

         pip install mechlab

   .. tab-item:: 🏗️ From Source
      :sync: source

      Best for contributors or those needing the "bleeding edge" version.

      .. code-block:: bash

         git clone https://github.com/sewaksunar/mechlab.git
         cd mechlab
         poetry install

---

Verify Installation
-------------------

To confirm that the mechanics and thermodynamics engines are correctly linked, run the following command in your terminal:

.. code-block:: bash

    python -c "import mechlab; print(f'✅ MechLab {mechlab.__version__} successfully initialized.')"

.. tip::
   **Stuck?** If you encounter issues with `NumPy` or `SciPy` binaries on Windows, ensure you have the `Microsoft Visual C++ Redistributable` installed.