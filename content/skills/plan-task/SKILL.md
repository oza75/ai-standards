---
name: plan-task
description: Decompose a task into reviewer-converged user stories before any code is written.
---

# plan-task

Decompose the given task into user stories, converge them through the `reviewer-loop`, then write the story files. No code is written until stories are reviewer-converged.

## Steps

1. **Read the working agreement** — understand the project's standards, stack, and constraints from `AGENTS.md`, `CLAUDE.md`, or equivalent.
2. **Explore the codebase** — understand what already exists, where the entry points are, and where the new work plugs in.
3. **Propose a story set** — decompose the task into independently implementable stories with: title, acceptance criteria, required tests, key files, and dependencies.
4. **Run the reviewer-loop** — fix every CRITICAL or MAJOR finding and re-propose until convergence.
5. **Write story files** — once converged, write each story under `docs/codes/tasks/<TASK>/user-stories/`.
6. **Run the reviewer-loop again** on the written files to confirm they match the converged proposals.

## Story file format

```markdown
---
code: <TASK>-<N>
title: "<short title>"
status: pending
created: <ISO date>
completed: ~
---

# <TASK>-<N> · <title>

**As a** <role>, **I want** <goal>, **so that** <benefit>.

## Acceptance Criteria
...

## Tests
...

## Key Files
...
```

## Rules

- Every story must be independently implementable with `test-driven-development`.
- Dependency order must be explicit in the task's `TASK.md`.
- Do not start coding until stories are reviewer-converged.
- A story that generates more than ~6 reviewer findings is too large — split it.
