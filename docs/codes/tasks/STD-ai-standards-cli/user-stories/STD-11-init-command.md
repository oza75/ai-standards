---
code: STD-11
title: "init command"
status: pending
created: 2026-06-24T00:00:00
completed: ~
---

# STD-11 · `init` command

**As a** user, **I want** `ai-standards init` to detect language, run all
adapters, and gitignore the deployed files in one step, **so that** a new
project is fully set up with one command.

## Acceptance Criteria

- Detects language from project dir (STD-3); `--python`/`--typescript`
  flags override
- Runs Claude Code, Cursor, and Copilot adapters; each receives the
  assembled layer dict and writes its files
- Collects all written paths from adapters; passes them to gitignore
  manager (STD-7) to add to `.gitignore` managed block
- If `~/.ai-standards/` is absent: prints clean message "Run
  `ai-standards install` first" and exits 1 (no traceback)
- If `{"typescript"}` detected: warns "TypeScript detected; no adapter
  available yet — deploying universal only" and continues
- Running twice is idempotent: same files, same gitignore block
- `--python` flag forces `{"python"}` layer regardless of detected
  language

## Tests

Functional (temp dir):
- `test_init_creates_all_adapter_files` — all expected files from STD-8,
  STD-9, STD-10 present after init
- `test_init_gitignores_all_files` — .gitignore managed block contains
  every path returned by adapters
- `test_init_python_flag_forces_python_layer` — --python flag; CLAUDE.local.md
  and python.mdc contain python layer content
- `test_init_not_installed_error` — missing ~/.ai-standards/ → exits 1
  with message containing "ai-standards install"; no traceback
- `test_init_typescript_warning` — TS-only project → stdout contains
  "no adapter" warning; universal files created; `.cursor/rules/python.mdc`
  does NOT exist
- `test_init_idempotent` — run twice; all files byte-identical; .gitignore
  has no duplicate entries

## Key Files

- `src/ai_standards/cli.py` — `init` subcommand
- `src/ai_standards/commands/init.py` — orchestrates detector + store +
  adapters + gitignore manager
