---
code: STD-9
title: "Cursor adapter"
status: pending
created: 2026-06-24T00:00:00
completed: ~
---

# STD-9 · Cursor adapter

**As a** user, **I want** the Cursor adapter to deploy `AGENTS.md`,
`.cursor/rules/python.mdc`, and `.cursor/skills/*/SKILL.md` so that my
standards and skills are available in every Cursor session.

## Pre-coding gate

**Before writing any test or code for this story:**
1. Fetch `cursor.com/docs/skills` and record the exact on-disk path for
   skills (`cursor/skills/<name>/SKILL.md` confirmed in round-1 research;
   verify and record the URL + retrieval date here before coding)
2. If the path has changed, update this story and rerun the reviewer

## Why each file

- `AGENTS.md` — Cursor reads this file as project-level agent instructions
  (per `cursor.com/docs/context/rules`). Contains universal layer content.
- `.cursor/rules/python.mdc` — `alwaysApply: true` ensures Python
  standards load in every Cursor session, not only when a `.py` file is
  open (glob-scoped loading would silently miss planning/general sessions)
- `.cursor/skills/plan-task/SKILL.md` and `review/SKILL.md` — Cursor
  skills loaded on demand via `@skill-name`

## Acceptance Criteria

- `AGENTS.md` created at project root with universal layer content
- `.cursor/rules/python.mdc` created **only when `"python" ∈ languages`**;
  frontmatter `alwaysApply: true` (no globs); body is python layer content
- When `"python" ∉ languages`: python.mdc is NOT written
- `.cursor/skills/plan-task/SKILL.md` created from
  `content/cursor/skills/plan-task/SKILL.md`
- `.cursor/skills/review/SKILL.md` created from
  `content/cursor/skills/review/SKILL.md`
- Never touches `.gitignore`
- Re-run overwrites all files cleanly
- Returns the list of written paths (varies based on languages)

## Tests

Unit:
- `test_creates_agents_md` — AGENTS.md exists at project root
- `test_agents_md_has_universal_content` — file contains universal layer text
- `test_creates_python_mdc_when_python_in_languages` — adapter called
  with `{"python"}`; .cursor/rules/python.mdc exists
- `test_no_python_mdc_when_python_absent` — adapter called with `{}`
  or `{"typescript"}`; `.cursor/rules/python.mdc` does NOT exist
- `test_python_mdc_frontmatter_always_apply` — parsed frontmatter has
  `alwaysApply: true` and no `globs` key
- `test_python_mdc_has_python_body` — file body contains python layer content
- `test_creates_plan_task_skill` — .cursor/skills/plan-task/SKILL.md exists
- `test_creates_review_skill` — .cursor/skills/review/SKILL.md exists
- `test_skill_name_matches_folder` — plan-task/SKILL.md frontmatter `name`
  equals `"plan-task"`; review/SKILL.md `name` equals `"review"` (Cursor
  requires name == parent folder name)
- `test_gitignore_not_touched` — .gitignore absent before and after adapter run
- `test_rerun_overwrites_cleanly` — run twice; files byte-identical
- `test_returns_written_paths_python` — with `{"python"}`, return includes
  exactly: AGENTS.md, .cursor/rules/python.mdc, .cursor/skills/plan-task/SKILL.md,
  .cursor/skills/review/SKILL.md (4 paths); with `{}`, return excludes
  python.mdc (3 paths)

## Key Files

- `src/ai_standards/adapters/cursor.py` — `CursorAdapter`
