# Contributing to mechlab

Thanks for considering a contribution.

## Setup

```bash
git clone https://github.com/sewaksunar/mechlab.git
cd mechlab
uv sync --extra dev --extra docs
```

## Before opening a PR

Run the same checks CI runs:

```bash
uv run ruff check src tests examples
uv run mypy
uv run pytest
```

All three must pass. If `ruff` finds fixable issues, run:

```bash
uv run ruff check src tests examples --fix
```

## Architecture rules

This project enforces strict one-directional dependencies:

```
interfaces -> application -> engine -> domain
```

A file in `domain/` must never import from `engine/`, `application/`,
or `interfaces/`. See `docs/architecture.md` for the full explanation
and for guidance on where new code belongs.

## Adding a new feature

1. Pure physics/math logic → `domain/`
2. Numerical algorithms/solvers → `engine/`
3. User-facing workflows → `application/`
4. CLI/report/plot output → `interfaces/`
5. Add tests under the matching `tests/<layer>/` directory
6. Add/update docstrings — the docs site is generated from them automatically

## Commit style

Keep commits focused and use clear, imperative messages (e.g.
"Add Truss body subclass", not "changes").

## Updating the changelog

Add an entry under `[Unreleased]` in `CHANGELOG.md` describing your change.
