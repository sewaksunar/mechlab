"""
application — orchestration layer. Wires domain objects + engine
solvers together into workflows a user can call in one or two lines.

This is the ONLY layer that should be considered "public API stable"
for most users. Internals of domain/engine may change more freely.

Contents:
    api.py        - BeamAnalysis and other high-level facade classes
    workflows.py  - multi-step analyses spanning several domain objects
    config.py     - application-level settings (tolerances, defaults)
"""
