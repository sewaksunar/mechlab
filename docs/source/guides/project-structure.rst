Project Structure
=================

This guide explains the MechLab module layout and how the codebase is organized
for a clean, modular workflow.

High-level layout
-----------------

- ``mechlab/api.py`` provides concise, user-facing helpers.
- ``mechlab/cli`` contains command-line entrypoints and subcommands.
- ``mechlab/core`` contains foundational math and unit utilities.
- ``mechlab/mechanics`` contains mechanics models and stress tools.
- ``mechlab/thermodynamics`` contains thermodynamic properties and cycles.
- ``mechlab/units`` centralizes unit registry and conversions.
- ``mechlab/display`` and ``mechlab/visual`` handle text, LaTeX, and plotting.
- ``mechlab/interactive`` contains Jupyter widgets.
- ``examples`` contains runnable scripts showcasing the API.

Design rules
------------

1. **Single source of truth**: Core computations live in one module and are
   reused by CLI, widgets, and exports.
2. **Thin adapters**: CLI and UI modules call core logic without duplicating it.
3. **Public API in ``mechlab/__init__.py``**: Top-level imports are stable.
4. **Docs follow code**: Public classes are documented in the API reference.

Stress workflow (example)
-------------------------

- Core stress logic lives in ``mechlab/mechanics/stress.py``.
- CLI and widgets import ``StressState`` from ``mechlab.mechanics``.
- ``mechlab/core/stress.py`` re-exports ``StressState`` for backward
  compatibility.
