---
code: STD-14
title: "shared skill content, store discovery, manifest paths"
status: done
created: 2026-06-24T00:00:00
completed: 2026-06-24T00:00:00
---

# STD-14 · Shared skill content, store discovery, manifest paths

**As a** user of any AI coding tool, **I want** all workflow skills to
live in a single tool-agnostic location, **so that** every adapter can
deploy the same canonical skill content without duplication.

## Acceptance Criteria

1. `CanonicalStore` gets a `get_skills() -> dict[str, str]` method that
   reads all manifest entries matching `content/skills/*/SKILL.md` and
   returns `{dirname: content}` — where `dirname` is the immediate parent
   directory name (e.g. `test-driven-development`).

2. Six SKILL.md files exist under `content/skills/`:
   - `plan-task` (rewritten from `content/cursor/skills/plan-task/`)
   - `review` (rewritten from `content/cursor/skills/review/`)
   - `test-driven-development` (new)
   - `reviewer-loop` (new)
   - `verification-before-completion` (new)
   - `systematic-debugging` (new)

3. Each SKILL.md has YAML frontmatter with `name:` equal to its directory
   name and a non-empty `description:`.

4. `layers/universal.md` has a **Workflow** section that names all 6
   skills and states when each is invoked. The skill names in this section
   match the frontmatter `name:` fields exactly (enforced by test).

5. Both `layers/manifest.json` and `src/ai_standards/manifest.json` list
   the 6 `content/skills/*/SKILL.md` paths and do NOT list:
   - any `content/cursor/skills/` path
   - `content/copilot/prompts/review.prompt.md`
   Both manifest files must stay byte-identical (same content, same copy
   operation as before).

6. `content/cursor/skills/` directory is removed entirely.

7. `content/copilot/prompts/review.prompt.md` is removed — its role is
   absorbed by `content/skills/review/SKILL.md`.

8. All tests that reference any of the removed or relocated paths are
   updated. Explicitly covers:
   - `tests/unit/test_adapter_content_files.py` (all cursor/skills and
     copilot/prompts/review.prompt.md references)
   - `tests/functional/test_update_command.py` (`_TEST_MANIFEST` hardcodes
     the old paths in lines 15–26)

## Tests

- `test_get_skills_returns_all_six` — `CanonicalStore.get_skills()` on
  real store (STORE_DIR = REPO_ROOT, MANIFEST_PATH = layers/manifest.json)
  returns exactly 6 entries with keys matching directory names.
- `test_skill_name_matches_directory` — for each skill, frontmatter
  `name:` equals the parent directory name.
- `test_workflow_section_references_all_skill_names` — the Workflow section
  in `layers/universal.md` contains every frontmatter `name:` value.
- `test_manifest_paths_match_actual_files` — every `content/skills/` entry
  in `layers/manifest.json` exists on disk, and every `content/skills/`
  file on disk is in the manifest (no orphans).

## Key Files

- `src/ai_standards/store.py` — add `get_skills()` method
- `content/skills/` — new directory (6 SKILL.md files)
- `content/cursor/skills/` — deleted
- `content/copilot/prompts/review.prompt.md` — deleted
- `layers/universal.md` — add Workflow section
- `layers/manifest.json` — update paths
- `src/ai_standards/manifest.json` — keep in sync with layers/manifest.json
- `tests/unit/test_adapter_content_files.py` — update path references
- `tests/functional/test_update_command.py` — update `_TEST_MANIFEST`
