---
code: STD-12
title: "sync command"
status: pending
created: 2026-06-24T00:00:00
completed: ~
---

# STD-12 · `sync` command

**As a** user, **I want** `ai-standards sync` to unconditionally
re-deploy all files from the canonical store, **so that** my project
reflects the latest standards after I update the canonical.

## Acceptance Criteria

- Re-runs all adapters; overwrites deployed files with current canonical
  content
- Does NOT touch `.gitignore` (files already gitignored from `init`)
- If `~/.ai-standards/` absent: exits non-zero with clean message
- Sync is unconditional overwrite — users edit the canonical repo, not
  the deployed files

## Tests

Functional (temp dir):
- `test_sync_restores_mutated_file` — mutate a deployed file; run sync;
  file restored to canonical content
- `test_sync_not_installed_error` — missing ~/.ai-standards/ → exits 1
  with clean message; no traceback
- `test_sync_does_not_touch_gitignore` — .gitignore byte-identical before
  and after sync

## Key Files

- `src/ai_standards/cli.py` — `sync` subcommand
- `src/ai_standards/commands/sync.py` — re-runs adapters only (no
  language detection, no gitignore)
