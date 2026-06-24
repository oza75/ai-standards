# ai-standards — working agreement

## What this project is

A portable Python CLI (`ai-standards`) that manages personal AI coding
standards across Claude Code, Cursor, and VS Code Copilot. Keeps a
canonical set of layer files in `~/.ai-standards/` and deploys them
per-project (gitignored) in each tool's native format.

Install: `uv tool install git+https://github.com/oza/ai-standards`

## How we work — the lifecycle

Every task is decomposed into **user stories** and built **test-first**.

1. Scope → Explore → Propose story set → **reviewer loop** (opus 4.8)
   until no CRITICAL/MAJOR → write story files → **reviewer loop** again
2. Implement one story at a time with `test-driven-development`:
   write failing test → watch it fail → minimal code to pass → refactor
3. Verify with `verification-before-completion` (`make check` must pass)
4. Reviewer loop on the code → mark story `done` → commit → merge

Reviewer agent: always use **claude-opus-4-8**. Loop until convergence
(no new CRITICAL/MAJOR findings).

Debug with `systematic-debugging` (root cause before any fix).

Task files: `docs/codes/tasks/[CODE]-[name]/` (`TASK.md` + `user-stories/`)

## Where code runs

This project runs **locally** (unlike bambara-gec which runs on a GPU box).
Use `uv run` directly. No SSH, no remote box.

```
make check    # ruff check + ruff format --check + mypy + pytest
make test     # pytest only
make lint     # ruff check + ruff format --check
```

## Current task

**Task STD — ai-standards CLI** — planning complete, ready to implement.

Stories: `docs/codes/tasks/STD-ai-standards-cli/user-stories/`

**Start here:** STD-1 (package scaffold) ∥ STD-2 (layer content) ∥ STD-2b (adapter content)

Implementation order:
```
STD-1 ∥ STD-2 ∥ STD-2b
  → STD-3 ∥ STD-4 ∥ STD-7
  → STD-5 → STD-6
  → STD-8 ∥ STD-9 ∥ STD-10
  → STD-11 → STD-12 → STD-13
```

Pre-coding gates required before STD-9 and STD-10 (verify Cursor skill
path and Copilot tool names against live docs — see the story files).

## Git

Conventional Commits. Branch per story: `<type>/STD-[N]-[short-name]`.
Trailer: `Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>`.

## Guardrails

- All deployed files are gitignored — personal standards, not team config
- TypeScript adapter out of scope for task STD (detector supports it,
  adapters do not)
- `clean`/`uninstall` and `status`/`list` commands deferred to follow-on task
