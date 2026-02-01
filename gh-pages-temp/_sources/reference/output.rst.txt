Output
======

Text display and export utilities.

.. automodule:: mechlab.output
   :members:
   :no-index:

Text Display
------------

.. autofunction:: mechlab.output.print_stress
   :no-index:

.. autofunction:: mechlab.output.print_beam
   :no-index:

.. autofunction:: mechlab.output.print_results
   :no-index:

Export
------

.. autofunction:: mechlab.output.export_csv
   :no-index:

.. autofunction:: mechlab.output.export_csv_table
   :no-index:

PDF Export
----------

.. note::

   PDF export requires the ``reportlab`` package:

   .. code-block:: bash

      pip install reportlab

.. py:function:: mechlab.output.export_pdf(results, filename, title="MechLab Analysis Report")

   Export analysis results to PDF file.

   :param results: Dictionary of result key-value pairs
   :param filename: Output PDF filename or path
   :param title: Report title (default: "MechLab Analysis Report")
