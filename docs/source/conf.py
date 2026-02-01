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
    "sphinx.ext.intersphinx",   # Cross-reference other projects
    "sphinx_copybutton",        # Adds "copy" button to code blocks
    "myst_parser",              # Allows you to write .md files
    "sphinx_design",            # Adds grids, buttons, and cards
]

# -- Intersphinx configuration -----------------------------------------------
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "matplotlib": ("https://matplotlib.org/stable/", None),
}

# -- Modular Automation Settings ---------------------------------------------
# Set to True to prevent duplicate page generation and fix "Double Vision"
autosummary_generate = True 

autodoc_typehints = "description"
add_module_names = True
autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'show-inheritance': True,
    'member-order': 'bysource',
}

# Support for Math in Markdown (MyST)
myst_enable_extensions = ["amsmath", "dollarmath"]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------
html_theme = "furo" 
html_title = "MechLab Documentation"
html_short_title = "MechLab"

html_static_path = ["_static"]
html_extra_path = ['.nojekyll']

# Custom CSS integration
def setup(app):
    app.add_css_file("custom.css")
    app.add_css_file("furo_overrides.css")

# Latest MathJax with better configuration
mathjax_path = "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"
mathjax3_config = {
    "tex": {
        "inlineMath": [["$", "$"], ["\\(", "\\)"]],
        "displayMath": [["$$", "$$"], ["\\[", "\\]"]],
    }
}

# -- Furo Theme Options ------------------------------------------------------
html_theme_options = {
    "source_repository": "https://github.com/sewaksunar/mechlab/",
    "source_branch": "main",
    "source_directory": "docs/source/",
    
    # Brand Colors
    "light_css_variables": {
        "color-brand-primary": "#2563eb", 
        "color-brand-content": "#1d4ed8",
        "color-foreground-primary": "#1f2937",
        "color-foreground-secondary": "#374151",
    },
    "dark_css_variables": {
        "color-brand-primary": "#60a5fa",
        "color-brand-content": "#3b82f6",
    },
    
    "sidebar_hide_name": False,
    "navigation_with_keys": True,
    "top_of_page_buttons": ["edit", "view"],
    "announcement": "<em>MechLab v0.2.4</em> – New consolidated modules for cleaner API!",
    
    "light_logo": "logo.png",
    "dark_logo": "logo.png",
    
    "toc_title_is_page_title": True,
    "source_edit_link": "https://github.com/sewaksunar/mechlab/edit/main/docs/source/{filename}",
    
    # Footer
    "footer_icons": [
        {
            "name": "GitHub",
            "url": "https://github.com/sewaksunar/mechlab",
            "html": """<svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 16 16"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.012 8.012 0 0 0 16 8c0-4.42-3.58-8-8-8z"/></svg>""",
            "class": "",
        },
    ],
}