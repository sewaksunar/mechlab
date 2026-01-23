import os
import sys
from datetime import datetime

# -- Path setup --------------------------------------------------------------
# Direct Sphinx to find the 'mechlab' source code
sys.path.insert(0, os.path.abspath("../../"))

# -- Project information -----------------------------------------------------
project = "MechLab"
copyright = f"{datetime.now().year}, Sewak Sunar"
author = "Sewak Sunar"

# -- General configuration ---------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",       # Pulls docs from your code
    "sphinx.ext.autosummary",   # Required for summary tables
    "sphinx.ext.napoleon",      # Support for NumPy/Google style docstrings
    "sphinx.ext.viewcode",      # Adds links to highlighted source code
    "sphinx.ext.mathjax",       # Renders LaTeX math in the browser
    "sphinx_copybutton",        # Adds "copy" button to code blocks
    "myst_parser",              # Allows you to write .md files
    "sphinx_design",            # Adds grids, buttons, and cards
]

# -- Modular Automation Settings ---------------------------------------------
# Set to True to prevent duplicate page generation and fix "Double Vision"
autosummary_generate = True 

autodoc_typehints = "description"
add_module_names = True

# Support for Math in Markdown (MyST)
myst_enable_extensions = ["amsmath", "dollarmath"]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------
html_theme = "furo" 
html_title = "MechLab Documentation"

html_static_path = ["_static"]
html_extra_path = ['.nojekyll']

# Custom CSS integration
def setup(app):
    app.add_css_file("custom.css")

# Latest MathJax
mathjax_path = "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"

# -- Furo Theme Options ------------------------------------------------------
html_theme_options = {
    "source_repository": "https://github.com/sewaksunar/mechlab/",
    "source_branch": "main",
    "source_directory": "docs/source/",
    
    # Brand Colors
    "light_css_variables": {
        "color-brand-primary": "#192bd0", 
        "color-brand-content": "#1c00e3",
    },
    "dark_css_variables": {
        "color-brand-primary": "#007fff",
        "color-brand-content": "#2196f3",
    },
    
    "sidebar_hide_name": False,
    "navigation_with_keys": True,
    
    # NOTE: 'collapse_navigation' and 'navigation_depth' removed 
    # as they are not supported by the Furo theme.
}