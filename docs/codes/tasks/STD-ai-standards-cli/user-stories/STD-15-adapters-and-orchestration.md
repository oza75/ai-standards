---
code: STD-15
title: "adapters and orchestration — AGENTS.md, commands, shared skills"
status: pending
created: 2026-06-24T00:00:00
completed: ~
---

# STD-15 · Adapters and orchestration — AGENTS.md, commands, shared skills

**As a** developer, **I want** `ai-standards init` and `sync` to deploy
shared skills to every tool's native location (Claude Code commands,
Cursor skills, Copilot prompts) and write AGENTS.md as a cross-tool
instruction file, **so that** all my AI tools get the same workflow
standards automatically.

## Acceptance Criteria

### ClaudeCodeAdapter

1. Signature: `run(project_dir: Path, layers: dict[str, str], skills: dict[str, str]) -> list[str]`
2. Writes `AGENTS.md` with the universal layer content only (no language layers).
3. Writes `CLAUDE.local.md` starting with `@AGENTS.md\n` followed by each
   language layer (no inline universal content — universal is imported via
   `@AGENTS.md`).
4. Writes `.claude/commands/<name>.md` for each `(name, content)` in skills.
5. Returns `["AGENTS.md", "CLAUDE.local.md", ".claude/commands/"]` — the
   directory entry `.claude/commands/` is used for gitignore (not per-file paths).

### CursorAdapter

6. Signature: `run(project_dir: Path, layers: dict[str, str], skills: dict[str, str]) -> list[str]`
7. Does **not** write `AGENTS.md` (it is now written by ClaudeCodeAdapter).
8. Writes `.cursor/skills/<name>/SKILL.md` for each `(name, content)` in skills.
9. Still writes `.cursor/rules/python.mdc` with `alwaysApply: true`
   frontmatter when `python` is in layers.
10. Returns only paths it writes (no AGENTS.md).

### CopilotAdapter

11. Signature: `run(project_dir: Path, layers: dict[str, str], reviewer_agent: str, skills: dict[str, str]) -> list[str]`
12. `review_prompt` parameter is removed — review content comes from the
    `review` entry in the skills dict.
13. Writes `.github/prompts/<name>.prompt.md` for each skill (including
    `review`), replacing the old dedicated `review.prompt.md`.
14. Still writes `.github/copilot-instructions.md` (universal layer) and
    `.github/agents/reviewer.agent.md`.

### Orchestration (init.py + sync.py)

15. Both `commands/init.py` and `commands/sync.py` call `store.get_skills()`
    and pass the result to all three adapters as the `skills` argument.
16. Neither command passes individual `skill_plan_task`, `skill_review`, or
    `review_prompt` arguments — those are gone.
17. Gitignore managed block includes `AGENTS.md` and `.claude/commands/` in
    addition to the existing entries from other adapters.
18. `update` is covered transitively through `sync` — no signature change
    needed for `commands/update.py`.

### Test updates

19. All existing adapter unit tests that assert the old behaviour are
    rewritten:
    - `tests/unit/test_claude_code_adapter.py` — CLAUDE.local.md inline
      universal becomes `@AGENTS.md` import; new AGENTS.md assertion; new
      commands dir assertion.
    - `tests/unit/test_cursor_adapter.py` — remove AGENTS.md assertion;
      update skill-path assertions.
    - `tests/unit/test_copilot_adapter.py` — remove `review_prompt` param;
      assert skills produce `.github/prompts/` files.
20. `tests/functional/test_init_command.py` is updated: `_EXPECTED_FILES`
    reflects the new layout (includes `AGENTS.md`, `.claude/commands/`,
    `.cursor/skills/<name>/SKILL.md` for each skill,
    `.github/prompts/<name>.prompt.md` for each skill; old per-skill paths
    like `.cursor/skills/plan-task/` and `.github/prompts/review.prompt.md`
    are replaced by the skills-dict-driven equivalents).

## Tests

- `test_claude_code_writes_agents_md` — AGENTS.md contains universal layer.
- `test_claude_local_starts_with_import` — CLAUDE.local.md first line is `@AGENTS.md`.
- `test_claude_code_deploys_commands_dir` — `.claude/commands/<name>.md`
  exists for each skill passed.
- `test_cursor_does_not_write_agents_md` — AGENTS.md absent after Cursor
  adapter runs alone.
- `test_cursor_deploys_all_skills` — `.cursor/skills/<name>/SKILL.md` for
  each skill.
- `test_copilot_deploys_skill_prompts` — `.github/prompts/<name>.prompt.md`
  for each skill.
- `test_init_deploys_skills_to_all_three_tools` (functional) — after `init`,
  asserts `.claude/commands/test-driven-development.md`,
  `.cursor/skills/test-driven-development/SKILL.md`,
  `.github/prompts/test-driven-development.prompt.md` all exist.

## Key Files

- `src/ai_standards/adapters/claude_code.py`
- `src/ai_standards/adapters/cursor.py`
- `src/ai_standards/adapters/copilot.py`
- `src/ai_standards/commands/init.py`
- `src/ai_standards/commands/sync.py`
- `tests/unit/test_claude_code_adapter.py`
- `tests/unit/test_cursor_adapter.py`
- `tests/unit/test_copilot_adapter.py`
- `tests/functional/test_init_command.py`

## Dependencies

STD-14 must be merged before starting STD-15.
