"""
interfaces — everything user- or system-facing: CLI commands, report
generation, plotting. This layer depends on `application`, and
through it, indirectly on `engine`/`domain` — but nothing below this
layer should ever import from here.

Contents:
    cli/      - command-line entry points
    output/   - report/export generation (text, csv, json)
    visual/   - plotting and diagrams (add as needed)
"""
