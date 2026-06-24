---
code: STD-6
title: "install command"
status: pending
created: 2026-06-24T00:00:00
completed: ~
---

# STD-6 · `install` command

**As a** user on a new machine, **I want** `ai-standards install` to
download the canonical layer files from GitHub to `~/.ai-standards/`,
**so that** other commands have content to deploy.

## Acceptance Criteria

Atomic download protocol (three-rename pattern — no data-loss window):
1. Download all files from the manifest to `~/.ai-standards.staging/`
2. If live dir exists: `os.rename(live, live.old)`
3. `os.rename(staging, live)` — same filesystem, near-instant
4. `shutil.rmtree(live.old)` if it exists

On any failure before step 3: `shutil.rmtree(staging)`. If process
crashes between steps 2 and 3, `.old/` preserves prior content;
`.staging/` has new content. Both are recoverable. This is the documented
accepted limitation.

- Reads manifest from the local repo (bundled); downloads exactly the
  listed files from `repo_url` on GitHub
- Second run produces byte-identical files in `~/.ai-standards/` and
  exits 0
- Mid-download network failure leaves `~/.ai-standards/` unchanged (or
  absent if first install); staging cleaned up
- `~/.ai-standards/layers/` and `~/.ai-standards/content/` have all
  expected files after success
- Non-zero exit with clear message on any download failure

## Tests

Unit:
- `test_downloads_all_manifest_files` — mock HTTP; verifies each manifest
  file is fetched and written to staging
- `test_second_run_is_idempotent` — mock HTTP returning fixed content;
  run install twice against same mock; second run exits 0 and files are
  byte-identical (mock ensures determinism, not live GitHub)
- `test_partial_download_leaves_live_unchanged` — mock network failure
  after first file; live dir intact (or absent); staging cleaned
- `test_staging_cleaned_on_failure` — after failure, no
  `~/.ai-standards.staging/` remains
- `test_all_expected_files_present_after_success` — post-install, every
  path in manifest exists under `~/.ai-standards/`

Note — unverified crash window: the crash-between-step-2-and-3 recovery
path (`.old/` has prior content, `.staging/` has new) is correct but has
no automated test. Manual verification: kill the process between the two
renames and confirm both dirs are intact. Future story may add a fault-
injection test once an appropriate hook exists.

Functional:
- `test_install_end_to_end` — real HTTP call to GitHub; all files
  downloaded; skip if `SKIP_NETWORK_TESTS` env var set

## Key Files

- `src/ai_standards/installer.py` — `Installer.run(manifest: Manifest, store_dir: Path) -> None`
- `src/ai_standards/cli.py` — `install` subcommand wired to `Installer`
