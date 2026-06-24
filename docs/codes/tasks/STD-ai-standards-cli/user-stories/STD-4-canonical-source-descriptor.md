---
code: STD-4
title: "Canonical source descriptor"
status: pending
created: 2026-06-24T00:00:00
completed: ~
---

# STD-4 · Canonical source descriptor

**As a** CLI command, **I want** a manifest that lists all expected file
paths, their source repo URL, and a version ref, **so that** `install`
and `update` know exactly what to fetch and can verify completeness.

## Acceptance Criteria

- `layers/manifest.json` exists in the repo
- Parses as valid JSON
- Contains `files`: list of all relative paths for layer files and
  content/ files (e.g. `"layers/universal.md"`,
  `"content/cursor/skills/plan-task/SKILL.md"`, …)
- Contains `repo_url`: string (e.g. `"https://github.com/oza/ai-standards"`)
- Contains `version_ref`: string (metadata only — `update` always
  re-downloads, no skip logic)
- `install` reads this manifest to know which files to fetch; it does not
  hard-code file paths

## Tests

Unit:
- `test_manifest_is_valid_json` — `layers/manifest.json` parses without
  error
- `test_manifest_has_files_list` — `files` key is a non-empty list of
  strings
- `test_manifest_lists_all_layer_files` — `files` contains entries for
  universal.md, python.md, typescript.md
- `test_manifest_lists_all_content_files` — `files` contains entries for
  all four content/ files (plan-task/SKILL.md, review/SKILL.md,
  reviewer.agent.md, review.prompt.md)
- `test_manifest_has_repo_url` — `repo_url` is a non-empty string
- `test_manifest_has_version_ref` — `version_ref` is a non-empty string
- `test_manifest_loader_raises_on_missing_fields` — loading a manifest
  missing `files`, `repo_url`, or `version_ref` raises `ManifestError`
  with a clear message

## Key Files

- `layers/manifest.json` — the descriptor (committed to repo)
- `src/ai_standards/manifest.py` — `Manifest` dataclass + `load_manifest(path: Path) -> Manifest`
