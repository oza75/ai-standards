---
code: STD-10
title: "VS Code Copilot adapter"
status: pending
created: 2026-06-24T00:00:00
completed: ~
---

# STD-10 · VS Code Copilot adapter

**As a** user, **I want** the Copilot adapter to deploy
`.github/copilot-instructions.md`, `.github/agents/reviewer.agent.md`,
and `.github/prompts/review.prompt.md`, **so that** my standards and
reviewer workflow are available in VS Code Copilot.

## Target

VS Code 1.102+ with GitHub Copilot extension.

## Pre-coding gate (Copilot agent tools)

**Before authoring `reviewer.agent.md` or writing its test:**
1. Fetch `https://code.visualstudio.com/docs/agent-customization/custom-agents`
   and `https://docs.github.com/en/copilot/reference/custom-agents-configuration`,
   record the exact valid tool identifiers + retrieval date here. The VS
   Code docs use namespaced names (`search/codebase`) while the GitHub
   reference uses bare names (`search`). Pin the authoritative source before
   coding — the test must assert the confirmed list, not an assumed one.
2. Fetch `https://docs.github.com/en/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot`
   and verify whether `applyTo` scoping in `.instructions.md` files works
   in local VS Code agent mode (as of docs retrieval date). If it does,
   the Python layer can be injected via a scoped instructions file instead
   of being absent from Copilot entirely. Record the finding here before
   coding STD-10.

## Why each file

- `.github/copilot-instructions.md` — always-on repo-level instructions;
  Copilot loads this automatically in every VS Code session. Contains
  universal layer content (language-specific not injected here since
  `applyTo` scoping is limited to cloud-agent/code-review surfaces only)
- `.github/agents/reviewer.agent.md` — custom Copilot reviewer subagent
  restricted to read-only tools; exact tool list confirmed in pre-coding gate
- `.github/prompts/review.prompt.md` — explicit `/review` invocation
  template; `name` frontmatter field is an authored convention (the
  platform uses filename as fallback if absent, but we set it explicitly
  so the invocation identifier is unambiguous)

## Acceptance Criteria

- `.github/copilot-instructions.md` created with universal layer content
- `.github/agents/reviewer.agent.md` created; frontmatter `tools` is the
  read-only list confirmed in pre-coding gate; body contains reviewer persona
- `.github/prompts/review.prompt.md` created; frontmatter `name` is
  non-empty (explicit convention, not a platform requirement)
- Never touches `.gitignore`
- Re-run overwrites all files cleanly
- Returns the list of written paths

## Tests

Unit:
- `test_creates_copilot_instructions` — .github/copilot-instructions.md exists
- `test_copilot_instructions_has_universal_content` — file contains
  universal layer text
- `test_creates_reviewer_agent` — .github/agents/reviewer.agent.md exists
- `test_reviewer_agent_tools_are_verified_list` — parsed frontmatter
  `tools` equals the list confirmed in pre-coding gate (reference a
  shared constant, not a hardcoded literal)
- `test_reviewer_agent_has_persona_body` — file body is non-empty
- `test_creates_review_prompt` — .github/prompts/review.prompt.md exists
- `test_review_prompt_has_name` — parsed frontmatter `name` is a
  non-empty string
- `test_gitignore_not_touched` — `.gitignore` absent before and after adapter run
- `test_rerun_overwrites_cleanly` — run twice; files byte-identical
- `test_returns_written_paths` — return value lists all three files

## Key Files

- `src/ai_standards/adapters/copilot.py` — `CopilotAdapter`
