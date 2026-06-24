---
code: STD-1
title: "Package scaffold"
status: pending
created: 2026-06-24T00:00:00
completed: ~
---

# STD-1 · Package scaffold

**As a** developer, **I want** an installable Python package skeleton,
**so that** `ai-standards --help` works and the project is ready for
feature development.

## Acceptance Criteria

- `pyproject.toml` declares one console-script entry point: `ai-standards`
- `uv run ai-standards --help` exits 0 and prints usage
- `uv run ai-standards install --help` exits 0 (subcommand registered)
- Package is installable via `uv tool install .`
- `mypy --strict`, `ruff check`, `ruff format --check`, `pytest` all pass
  on an empty test suite

## Tests

Unit:
- `test_cli_help_exits_zero` — invoking `ai-standards --help` via
  `subprocess` exits with code 0 and stdout contains "Usage"
- `test_install_subcommand_registered` — `ai-standards install --help`
  exits 0

Functional:
- `test_package_installable` — `uv tool install .` in a temp venv exits 0

## Key Files

- `pyproject.toml` — package metadata, `[project.scripts]`, dev deps
- `src/ai_standards/__init__.py` — package root
- `src/ai_standards/cli.py` — entry point, top-level CLI group
- `Makefile` — `check`, `test`, `lint` targets
