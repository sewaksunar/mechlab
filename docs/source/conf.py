import os
import sys

sys.path.insert(0, os.path.abspath("../../"))

project = "MechLab"
author = "Sewak Sunar"
release = "0.1.0"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx_autodoc_typehints",
]

autosummary_generate = True

html_theme = "furo"
