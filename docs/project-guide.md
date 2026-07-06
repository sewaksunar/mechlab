# Project Guide

This guide is for someone who understands mechanics and wants a practical way to work on the code without needing to be a full-time software developer.

---

## What MechLab Is

MechLab is a modular engineering mechanics library. The working example today is beam analysis, but the structure supports future topics: trusses, shafts, dynamics, and design checks.

At a high level, the library takes physical inputs (material properties, geometry, supports, loads), solves the structure, computes internal responses, and formats results for the CLI, reports, plots, or Python scripts.

---

## Project Structure

The repository is organized by **responsibility**, not by feature size.

=== "Source Code"

    ```text
    src/mechlab/
    ├── domain/       ← pure engineering objects and rules
    ├── engine/       ← numerical methods and unit handling
    ├── application/  ← user-facing workflows and public API
    ├── interfaces/   ← CLI, reports, and plotting
    └── shared/       ← small helpers used across layers
    ```

=== "Project Root"

    ```text
    docs/              documentation source (MkDocs)
    tests/             tests grouped to match code layers
    examples/          small runnable scripts
    README.md          quick project overview
    CONTRIBUTING.md    contributor workflow
    pyproject.toml     package metadata and tooling config
    ```

---

## Architecture

The code follows a strict **one-way dependency flow**:

```text
interfaces → application → engine → domain
```

Lower layers never import from higher layers.

| Layer | Responsibility | Key modules |
| :--- | :--- | :--- |
| `domain/` | Engineering concepts: `Material`, `Section`, `Load`, `Support`, `Beam` | `entities.py`, `strength/beam.py` |
| `engine/` | Math and solving logic | `math/solvers.py` |
| `application/` | Public facade: `BeamAnalysis` | `api.py`, `workflows.py` |
| `interfaces/` | Presentation: CLI, text reports, plots | `cli/commands.py`, `output/report.py`, `visual/plots.py` |

!!! info "Why this matters"
    This separation makes the core mechanics easy to test, easy to extend, and reusable across different interfaces.

---

## How the Library Works

``` mermaid
graph LR
    A[Create Material & Section] --> B[Build BeamAnalysis]
    B --> C[Add supports & loads]
    C --> D[Call run]
    D --> E[Read results or format output]
    E --> F[Optionally plot diagrams]
```

??? abstract "Key classes at a glance"

    | Class | Purpose |
    | :--- | :--- |
    | `mechlab.domain.entities.Material` | Young's modulus, yield strength |
    | `mechlab.domain.entities.Section` | Inertia, area, extreme fiber distance |
    | `mechlab.domain.entities.PointLoad` / `DistributedLoad` / `PointMoment` | Load definitions |
    | `mechlab.domain.entities.Support` / `SupportType` | Boundary conditions |
    | `mechlab.domain.strength.beam.Beam` | The beam object itself |
    | `mechlab.application.api.BeamAnalysis` | Public API facade |
    | `mechlab.engine.math.solvers.MatrixBeamSolver` | Matrix-based beam solver |
    | `mechlab.interfaces.output.report.ReportGenerator` | Text output |
    | `mechlab.interfaces.visual.plots` | Shear, moment, FBD diagrams |

!!! note
    The solver currently used by `Beam` is the matrix-based solver. A simpler two-support equilibrium solver also exists in `engine/math/solvers.py` as a reference.

---

## How to Use It

### Install for development

```bash
uv sync --extra dev --extra docs
```

### Run the example

```bash
PYTHONPATH=src python examples/simply_supported_beam.py
```

### Run tests

```bash
uv run pytest
```

### Live preview docs

```bash
uv run mkdocs serve
```

!!! tip
    `mkdocs serve` starts a local server with auto-reload. Use `mkdocs build` only when you need a deployable static site.

### Lint and type checks

```bash
uv run ruff check src tests examples
uv run mypy
```

### Use the CLI

```bash
uv run python -m mechlab beam \
  --length 4.0 \
  --E 200e9 \
  --yield 250e6 \
  --I 9.19e-6 \
  --area 2.3e-3 \
  --c 0.076 \
  --support 0.0 \
  --support 4.0 \
  --point-load 2.0 5000
```

### Package and publish

```bash
uv build      # creates sdist + wheel locally
uv publish    # uploads to PyPI
```

!!! warning "PyPI authentication"
    PyPI no longer accepts account passwords.

    - Use `__token__` as the username and paste your **API token** as the password.
    - Or configure [Trusted Publishers](https://docs.pypi.org/trusted-publishers/) on PyPI + GitHub.
    - Make sure version, changelog, tests, and docs are updated before publishing.

---

## How to Add a Feature

First, decide where it belongs:

| If it's a... | It goes in... |
| :--- | :--- |
| Pure mechanics rule or data model | `domain/` |
| Solver or numerical method | `engine/` |
| User workflow or facade | `application/` |
| CLI command, report, or plot | `interfaces/` |

Then follow the same pattern every time:

1. Add the smallest useful implementation in the right layer.
2. Add a test in the matching test folder.
3. Update examples or docs if usage changes.
4. Keep the public API stable when possible.
5. Add a changelog entry if the change is user-visible.

??? example "Examples of where things go"

    - **New load type** → `domain/entities.py`, then teach the solver to handle it.
    - **New workflow** → `application/workflows.py` if it's a full analysis step.
    - **New CLI command** → `interfaces/cli/commands.py`.
    - **New plot** → `interfaces/visual/plots.py`.

---

## How to Improve the Library

=== "Engineering improvements"

    - Add more load types (triangular distributed, applied couples)
    - Add more support types with clear boundary-condition validation
    - Improve input checking so invalid spans, positions, and units fail early
    - Expand beyond beams: trusses, shafts, frames
    - Add more outputs: deflection, slope, stress envelopes, design checks
    - Keep units explicit and consistent everywhere

=== "Software improvements"

    - Prefer small classes with one responsibility
    - Keep functions short and testable
    - Put validation close to the data model
    - Use type hints consistently
    - Make interfaces stable and simple for non-software users
    - Add tests for edge cases, not only happy paths
    - Reduce repeated code in beam domain and solver logic
    - Keep plot and CLI layers thin so core calculations stay reusable

---

## How to Contribute

!!! quote "Golden rule"
    Contributions are easiest when they stay local to **one layer at a time**.

**Recommended steps:**

1. Create a feature branch.
2. Make one focused change.
3. Run the checks that match your change.
4. Update tests and docs together.
5. Commit with a clear message.
6. Open a pull request describing what changed and why.

**Before opening a PR:**

```bash
uv run ruff check src tests examples
uv run mypy
uv run pytest
```

If the change affects user-facing behavior, also update `CHANGELOG.md` and the docs.

---

## Git Workflow

1. Sync your branch with the latest `main`.
2. Create a feature branch for one topic only.
3. Keep commits small and descriptive.
4. Run checks before each commit.
5. Push the branch and open a pull request.
6. Merge only after tests, linting, and type checks pass.

!!! example "Good commit messages"
    - `Add point moment support to beam analysis`
    - `Improve CLI error message for invalid support count`
    - `Document solver flow for beam workflows`

---

## Mental Model

If you're coming from mechanical engineering:

| Layer | Think of it as... |
| :--- | :--- |
| `domain/` | The textbook model of the structure |
| `engine/` | The mathematics that solves it |
| `application/` | The lab assistant who collects inputs and runs the procedure |
| `interfaces/` | The way you talk to the program |

This mental model makes it straightforward to decide where any new feature belongs.

---

## Suggested Next Reads

- [Architecture](architecture.md) for dependency rules and layering
- [Getting Started](getting-started.md) for the quickest path to running the library
- [CLI Reference](cli.md) for command-line usage
- [API Reference](reference/domain.md) for auto-generated docs from code
```

**What's improved:**

- **Tabbed code blocks** for project structure (source vs root) instead of back-to-back walls of text
- **Mermaid diagram** for the analysis flow (renders natively with your superfences config)
- **Collapsible sections** (`??? abstract`, `??? example`) to hide detail until needed
- **Tables** instead of bullet lists wherever there's a mapping (layer → responsibility, class → purpose)
- **Admonitions** (`!!! warning`, `!!! tip`, `!!! info`) for callouts that actually stand out visually
- **Tabbed sections** for engineering vs software improvements so readers only see what's relevant to them
- Tighter copy throughout, no filler paragraphs