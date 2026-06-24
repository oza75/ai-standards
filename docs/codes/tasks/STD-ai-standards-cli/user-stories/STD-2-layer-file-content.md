---
code: STD-2
title: "Layer file content"
status: pending
created: 2026-06-24T00:00:00
completed: ~
---

# STD-2 · Layer file content

**As a** user, **I want** the canonical layer files authored and stored
under `layers/` in this repo, **so that** they are ready to be installed
and deployed to projects.

## Acceptance Criteria

- `layers/universal.md` exists and contains sections: Naming, Docs,
  Tests, Git
- `layers/python.md` exists and contains sections: Typing, Async-Sync,
  Tools; those section headings are absent from `universal.md`
- `layers/typescript.md` exists, contains sections Naming, Typing, Tests,
  and is clearly marked as a stub (e.g. `> Stub — TypeScript adapter not
  yet implemented`)
- All three files are valid UTF-8 Markdown (no binary chars, no null
  bytes)

## Tests

Unit:
- `test_universal_has_required_sections` — universal.md contains headings
  for Naming, Docs, Tests, Git
- `test_python_has_required_sections` — python.md contains Typing,
  Async-Sync, Tools
- `test_python_sections_absent_from_universal` — universal.md does not
  contain the headings Typing, Async-Sync, Tools
- `test_typescript_has_required_sections` — typescript.md contains
  Naming, Typing, Tests
- `test_typescript_marked_as_stub` — typescript.md contains the word
  "Stub" (case-insensitive)
- `test_all_layer_files_are_utf8` — each file decodes cleanly as UTF-8

## Key Files

- `layers/universal.md` — process, naming, docs, tests, git (language-agnostic)
- `layers/python.md` — Python-specific: typing, async/sync, tools
- `layers/typescript.md` — TypeScript stub
