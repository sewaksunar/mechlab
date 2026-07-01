# Changelog

All notable changes to this project are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

## [0.1.0] - 2026-07-01
### Added
- Initial layered architecture: `domain`, `engine`, `application`, `interfaces`, `shared`.
- `Body` abstract base class; `Beam` concrete implementation for simply-supported beam analysis.
- `EquilibriumSolver` for two-support reaction calculations.
- `UnitRegistry` for SI unit conversion.
- `BeamAnalysis` application facade with fluent/chainable API.
- CLI entry point: `python -m mechlab beam ...`.
- Full test suite covering domain, engine, and application layers.
- MkDocs + mkdocstrings documentation site with light/dark theme toggle.
- CI pipeline: ruff lint, mypy type check, pytest across Python 3.9–3.12.
