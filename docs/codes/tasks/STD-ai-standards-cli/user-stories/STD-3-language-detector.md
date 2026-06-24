---
code: STD-3
title: "Language detector"
status: pending
created: 2026-06-24T00:00:00
completed: ~
---

# STD-3 · Language detector

**As a** CLI command, **I want** to detect the language(s) of a project
directory, **so that** `init` deploys the right layers without requiring
an explicit flag.

## Acceptance Criteria

Detection rules (checked in this order):
- `pyproject.toml` or `setup.py` present → `{"python"}`
- `package.json` present with `"typescript"` in dev/direct deps → `{"typescript"}`
  (TypeScript supersedes JavaScript — no separate JS layer exists)
- `package.json` present without typescript dep → `{}` (warn: "No layer
  for JavaScript; deploying universal only")
- Both Python and TypeScript manifests present → `{"python", "typescript"}`
- Neither → `{}` (warn: "No language detected; deploying universal only")

Explicit flags replace (not add to) the detected set:
- `--python` → `{"python"}`
- `--typescript` → `{"typescript"}`
- `--python --typescript` → `{"python", "typescript"}`

## Tests

Unit:
- `test_detects_python_from_pyproject` — dir with pyproject.toml → `{"python"}`
- `test_detects_python_from_setup_py` — dir with setup.py only → `{"python"}`
- `test_detects_typescript_from_package_json` — package.json with
  `"typescript"` in dependencies → `{"typescript"}`
- `test_js_only_returns_empty` — package.json without typescript dep →
  `set()` (no JS layer)
- `test_detects_both` — pyproject.toml + package.json with typescript → `{"python","typescript"}`
- `test_neither_returns_empty` — empty dir → `set()`
- `test_flag_replaces_detected_python` — `--python` flag in TS project → `{"python"}`
- `test_flag_replaces_detected_typescript` — `--typescript` in Python project → `{"typescript"}`
- `test_both_flags` — `--python --typescript` → `{"python","typescript"}`

## Key Files

- `src/ai_standards/detector.py` — `detect_languages(project_dir: Path, flags: set[str]) -> set[str]`
