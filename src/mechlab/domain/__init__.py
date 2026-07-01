"""
domain — pure engineering science. NO I/O. NO external dependencies.

Everything here should be understandable and testable by a mechanical
engineer with zero knowledge of software architecture. If a class in
this package needs to read a file, print something, or call a solver
library directly, it belongs in a different layer.

Contents:
    entities.py   - Body (abstract base), Material, Section, Load hierarchy, Support
    strength/     - concrete Body subclasses for mechanics-of-materials analysis
"""
