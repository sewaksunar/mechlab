"""
mechlab — a modular, object-oriented engineering mechanics library.

ARCHITECTURE OVERVIEW
======================
This package is organized into four layers. Dependencies only ever
flow DOWNWARD — a layer may import from the layers below it, never
from the layers above it. This keeps the core physics/math testable
in total isolation from I/O, CLI, or plotting concerns.

    interfaces/   -> how users/systems interact (CLI, reports, plots)
    application/   -> orchestrates domain + engine into workflows
    engine/        -> numerical machinery (solvers, units, math)
    domain/        -> pure engineering science (Body, Beam, Load, ...)

Rule of thumb: if you're not sure where new code belongs, ask
"does this know about physics?" -> domain. "Does this know about
algorithms/numbers?" -> engine. "Does this coordinate steps for a
user?" -> application. "Does this touch a terminal/file/screen?"
-> interfaces.

PUBLIC API
==========
Most users only need this:

    from mechlab import BeamAnalysis

    result = (
        BeamAnalysis(length=4.0, material=steel, section=i_beam)
        .set_simple_supports(0.0, 4.0)
        .add_point_load(2.0, 5000)
        .run()
    )

For lower-level access (custom solvers, new Body subclasses), import
directly from `mechlab.domain` / `mechlab.engine`.
"""

from mechlab.application.api import BeamAnalysis

__all__ = ["BeamAnalysis"]
__version__ = "0.1.0"
