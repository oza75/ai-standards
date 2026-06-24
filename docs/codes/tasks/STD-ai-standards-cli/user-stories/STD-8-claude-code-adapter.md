---
code: STD-8
title: "Claude Code adapter"
status: pending
created: 2026-06-24T00:00:00
completed: ~
---

# STD-8 · Claude Code adapter

**As a** user, **I want** the Claude Code adapter to deploy
`CLAUDE.local.md` so that my personal AI coding standards are
automatically loaded by Claude Code in any project.

## Why CLAUDE.local.md

`CLAUDE.local.md` is the documented gitignored personal slot in Claude
Code's memory hierarchy: "Personal project-specific preferences. Add to
.gitignore." It is auto-loaded alongside the project's committed
`CLAUDE.md`. This separates personal standards (gitignored, this tool
manages) from project standards (committed, project team manages).

Claude Code does NOT read `AGENTS.md` — that file is deployed by the
Cursor adapter (STD-9) for Cursor's use.

## Acceptance Criteria

- `CLAUDE.local.md` created at project root
- Contains the universal layer content followed by the language-specific
  layer content (separated by a blank line)
- Never modifies any committed `CLAUDE.md` at project root or
  `.claude/CLAUDE.md`
- Never touches `.gitignore` (only `init` does, via STD-7)
- Re-run overwrites `CLAUDE.local.md` cleanly (sync behavior)
- Returns the list of written paths (consumed by `init` to gitignore them)

## Tests

Unit:
- `test_creates_claude_local_md` — adapter called on temp dir with python
  layer → `CLAUDE.local.md` exists
- `test_claude_local_contains_universal` — file contains universal layer
  content
- `test_claude_local_contains_language_layer` — file contains python
  layer content when `"python"` in language set
- `test_claude_local_universal_only_when_no_language` — adapter called
  with empty language set → CLAUDE.local.md contains universal content
  and does NOT contain python layer content
- `test_does_not_touch_committed_claude_md` — if `CLAUDE.md` exists,
  it is byte-identical before and after adapter run
- `test_gitignore_not_touched` — `.gitignore` absent before and after
  adapter run
- `test_rerun_overwrites_cleanly` — run twice; second run produces same
  content, exits 0
- `test_returns_written_paths` — return value is `[Path("CLAUDE.local.md")]`

## Key Files

- `src/ai_standards/adapters/claude_code.py` — `ClaudeCodeAdapter`
