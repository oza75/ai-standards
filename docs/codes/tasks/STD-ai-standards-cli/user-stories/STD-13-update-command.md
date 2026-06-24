---
code: STD-13
title: "update command"
status: pending
created: 2026-06-24T00:00:00
completed: ~
---

# STD-13 · `update` command

**As a** user, **I want** `ai-standards update` to pull the latest
canonical from GitHub and then re-deploy to the current project, **so
that** both the store and the project files are current in one step.

## Acceptance Criteria

- Calls `install` (re-downloads all canonical files to `~/.ai-standards/`
  using the three-rename protocol from STD-6)
- Then calls `sync` (re-deploys from updated canonical to current project)
- Network failure during install: exits non-zero with clean message;
  `~/.ai-standards/` unchanged (install atomicity guarantee from STD-6);
  subsequent `sync` still works from the prior canonical
- Always re-downloads (no version comparison — `version_ref` is metadata only)

## Tests

Functional (temp dir):
- `test_update_redeploys_files` — mock GitHub returning updated layer
  content; after update, deployed files contain the new content
- `test_update_network_failure_leaves_store_intact` — mock network
  failure; `~/.ai-standards/` content unchanged; exits 1 with clean message
- `test_update_failure_does_not_corrupt_deployed_files` — after a failed
  update, existing deployed files are byte-identical to pre-update state
- `test_sync_still_works_after_failed_update` — after failed update,
  `sync` runs successfully from prior canonical

## Key Files

- `src/ai_standards/cli.py` — `update` subcommand
- `src/ai_standards/commands/update.py` — calls `Installer.run()` then
  `sync` command logic
