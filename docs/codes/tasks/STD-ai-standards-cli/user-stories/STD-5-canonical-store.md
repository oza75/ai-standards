---
code: STD-5
title: "Canonical store"
status: pending
created: 2026-06-24T00:00:00
completed: ~
---

# STD-5 · Canonical store

**As a** CLI adapter, **I want** to read and assemble layer content from
`~/.ai-standards/`, validated against the manifest, **so that** deploy
commands have correct content to write.

## Acceptance Criteria

- `CanonicalStore` reads from `~/.ai-standards/`
- Raises `NotInstalledError` (clean user message + non-zero exit) when
  `~/.ai-standards/` is absent
- Raises `NotInstalledError` when installed files don't match the
  manifest (incomplete install)
- `assemble_layers(languages: set[str]) -> dict[str, str]` returns a
  dict keyed by exact strings `"universal"`, `"python"`, `"typescript"`;
  always includes `"universal"`; includes language keys for requested
  languages
- `get_content(relative_path: str) -> str` returns verbatim content of
  a file under `~/.ai-standards/content/`; content files are NOT in the
  layer dict

## Tests

Unit:
- `test_raises_not_installed_when_absent` — `CanonicalStore` with missing
  dir raises `NotInstalledError`; message is human-readable (contains
  "ai-standards install")
- `test_raises_on_incomplete_install` — store missing a file listed in
  manifest raises `NotInstalledError`
- `test_assembles_universal_always` — `assemble_layers(set())` returns
  `{"universal": <content>}`
- `test_assembles_python_layer` — `assemble_layers({"python"})` returns
  dict with keys `"universal"` and `"python"`
- `test_get_content_returns_file_text` — `get_content("content/cursor/skills/plan-task/SKILL.md")`
  returns the file's text
- `test_content_not_in_layer_dict` — layer dict keys never include
  `"content/..."` paths

## Key Files

- `src/ai_standards/store.py` — `CanonicalStore`, `NotInstalledError`
- `src/ai_standards/manifest.py` — `Manifest` (from STD-4)
