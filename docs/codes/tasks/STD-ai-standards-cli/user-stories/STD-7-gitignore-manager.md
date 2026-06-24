---
code: STD-7
title: "Gitignore manager"
status: pending
created: 2026-06-24T00:00:00
completed: ~
---

# STD-7 · Gitignore manager

**As a** CLI command, **I want** to add and remove generated file paths
to/from `.gitignore` using a managed block, **so that** standards files
are never accidentally committed and future cleanup is possible.

## Acceptance Criteria

- Inserts a delimited managed block:
  ```
  # BEGIN ai-standards
  <paths>
  # END ai-standards
  ```
- Running again with the same paths: file unchanged (idempotent)
- Running with a different path list: only the managed block changes;
  content outside the block is untouched
- Creates `.gitignore` if absent
- `remove_block(gitignore: Path) -> None` deletes the entire managed
  block and leaves the rest of the file intact
- Adapters (STD-8, STD-9, STD-10) never call the gitignore manager
  directly — only `init` does

## Tests

Unit:
- `test_inserts_managed_block` — empty .gitignore + paths list → file
  contains BEGIN/END markers with paths inside
- `test_idempotent_same_paths` — calling with same paths twice → file
  byte-identical after second call
- `test_replaces_block_with_new_paths` — calling with different paths
  replaces only the managed block; content outside block preserved
- `test_creates_gitignore_if_absent` — no .gitignore exists → created
  with managed block
- `test_remove_block_deletes_block` — file with managed block + other
  content → after remove_block, block gone, other content intact
- `test_remove_block_noop_when_absent` — file with no managed block →
  remove_block exits 0, file unchanged

## Key Files

- `src/ai_standards/gitignore.py` — `GitignoreManager` with
  `add_paths(gitignore: Path, paths: list[str]) -> None` and
  `remove_block(gitignore: Path) -> None`
