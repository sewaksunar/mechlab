Installation
============

MechLab is a Python-based engineering library. We recommend installing it within a virtual environment to manage dependencies safely.

.. tab-set::

   .. tab-item:: 📦 Poetry
      
      This is the recommended way to install MechLab for project development.

      .. code-block:: bash

         poetry add mechlab

   .. tab-item:: 🐍 Pip
      
      Standard installation for quick scripts or Google Colab.

      .. code-block:: bash

         pip install mechlab

   .. tab-item:: 🏗️ From Source
      
      For contributors who want to modify the mechanics or thermo engines.

      .. code-block:: bash

         git clone https://github.com/sewaksunar/mechlab.git
         cd mechlab
         poetry install

---

Verify Installation
-------------------

After installation, verify that the engineering modules are accessible by running this in your terminal:

.. code-block:: bash

   python -c "import mechlab; print(f'MechLab {mechlab.__version__} initialized.')"

.. note: ⚠️ Prerequisites
   :class-card: sd-bg-light
   
   * **Python:** 3.9 or higher
   * **Operating System:** Windows, macOS, or Linux
   * **Core Dependencies:** NumPy, SciPy, SymPy