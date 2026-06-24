---
code: STD-2b
title: "Tool adapter content files"
status: pending
created: 2026-06-24T00:00:00
completed: ~
---

# STD-2b · Tool adapter content files

**As a** CLI adapter, **I want** authored content files for Cursor skills
and Copilot agent/prompt under `content/`, **so that** adapters can
deploy them verbatim without generating content from layer data.

## Pre-coding gate (Copilot agent tools)

**Before authoring `reviewer.agent.md`:**
Fetch `https://code.visualstudio.com/docs/agent-customization/custom-agents`
and record the exact valid tool identifiers + retrieval date here.
The VS Code docs use namespaced names (e.g. `search/codebase`, `edit`)
while the GitHub Copilot reference uses bare names (`read`, `search`).
The two are internally inconsistent; pin the authoritative source and
the exact list before writing the file or its test.

## Acceptance Criteria

- `content/cursor/skills/plan-task/SKILL.md` exists; frontmatter `name`
  equals `"plan-task"` (must match the parent folder name, per Cursor
  docs) and `description` is present
- `content/cursor/skills/review/SKILL.md` exists; frontmatter `name`
  equals `"review"`; `description` present
- `content/copilot/agents/reviewer.agent.md` exists; frontmatter has
  `name`, `description`, and `tools` set to the valid read-only tool
  list confirmed in the pre-coding gate above
- `content/copilot/prompts/review.prompt.md` exists; frontmatter has
  `name` — chosen convention to make the invocation identifier explicit
  (the platform uses filename as fallback if `name` is absent, but we
  author it explicitly for clarity)
- All files are valid UTF-8 Markdown

## Tests

Unit:
- `test_plan_task_skill_name_matches_folder` — plan-task/SKILL.md
  frontmatter `name` equals `"plan-task"` exactly (not just regex)
- `test_review_skill_name_matches_folder` — review/SKILL.md frontmatter
  `name` equals `"review"` exactly
- `test_skill_descriptions_present` — both SKILL.md files have non-empty
  `description` field
- `test_reviewer_agent_tools_are_verified_list` — reviewer.agent.md
  frontmatter `tools` equals the list confirmed in the pre-coding gate
  (test must reference a constant, not a hardcoded literal, so updating
  the list updates the test)
- `test_review_prompt_has_name` — review.prompt.md frontmatter `name` is
  a non-empty string
- `test_all_content_files_are_utf8` — each file decodes cleanly as UTF-8

## Key Files

- `content/cursor/skills/plan-task/SKILL.md` — planning skill for Cursor
- `content/cursor/skills/review/SKILL.md` — convergence-loop review skill
- `content/copilot/agents/reviewer.agent.md` — Copilot reviewer persona
- `content/copilot/prompts/review.prompt.md` — Copilot /review prompt
