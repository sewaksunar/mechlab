import os
import sys
# Move up to the root where the 'mechlab' folder sits
sys.path.insert(0, os.path.abspath('../../'))

# -- Project information -----------------------------------------------------
project = 'MechLab'
copyright = '2026, sewaksunar'
author = 'sewaksunar'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon', # Supports Google/NumPy style docstrings
    'sphinx.ext.githubpages',
]

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
html_theme = 'furo'  # The modern UI theme
html_title = "MechLab Documentation"

html_theme_options = {
    "sidebar_hide_name": False,
    "navigation_with_keys": True,
    "source_repository": "https://github.com/sewaksunar/mechlab/",
    "source_branch": "main",
    "source_directory": "docs/source/",
}

# Add any custom CSS here if needed
html_static_path = ['_static']