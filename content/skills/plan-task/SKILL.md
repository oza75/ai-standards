---
name: plan-task
description: Use before any code is written — decompose a goal into reviewer-converged user stories and write the story files. Planning only; hand off to implement-story to build them.
---

# plan-task

The **planning** half of the lifecycle: turn a goal into a reviewer-converged set
of written user stories, built to be implemented **test-first**. This skill stops
at a plan — it does not write production code. When the stories are converged and
written, hand off to `implement-story` to build them.

Planning is a **loop**: propose → review → revise, until the decomposition
converges. Write no story files, and no code, before the story set converges.

## Phase 1 — Scope

State the task outcome, why it exists, and its constraints. Source it from the
project roadmap or the request. Assign a short task code and a kebab name →
folder `docs/codes/tasks/[CODE]-[short-name]/`.

## Phase 2 — Explore

Find existing code, patterns, and utilities to reuse **before** proposing
anything new. Note what must stay untouched (invariants, guardrails, data that
must not be modified).

## Phase 3 — Propose the story set (no files yet)

Draft the candidate stories: title, a one-line "As a / I want / so that", the
rough tests each implies, and dependencies. Aim for INVEST stories —
independent, negotiable, valuable, estimable, small, testable.

## Phase 4 — Reviewer gate #1 (the story set)

Hand the decomposition to `reviewer-loop`. Challenge the **choice and
boundaries**: missing or redundant stories, wrong sizing, untestable stories,
mis-ordered dependencies, coverage gaps. **Loop — revise and re-review — until it
converges** (no CRITICAL/MAJOR). **Write no files before this converges.**

## Phase 5 — Write the task and stories

Write `TASK.md` and one file per story. Every story carries its **test list**
(unit + functional) — tests are part of the specification because the work is
built test-first.

## Phase 6 — Reviewer gate #2 (the written stories)

Run `reviewer-loop` on the written stories — acceptance criteria, test lists,
key files, against the project's standards. Loop to convergence.

## Done — hand off to implementation

Planning is complete when the stories are written and reviewer-converged. Do
**not** start coding here. Hand off to `implement-story`, which takes the stories
one at a time through the coding loop (TDD → verification → review → commit).

## File formats

`docs/codes/tasks/[CODE]-[short-name]/TASK.md`:

```markdown
# [CODE] · [Title]

## Context
<why this task exists, current state, goal, constraints>

## User Stories
- [[CODE]-1 — Title](user-stories/[CODE]-1-[name].md)
- …
```

`…/user-stories/[CODE]-[N]-[short].md`:

```markdown
---
code: [CODE]-[N]
title: "[Story title]"
status: pending          # pending | progress | done
created: [YYYY-MM-DDThh:mm:ss]
completed: ~
---

# [CODE]-[N] · [Story title]

**As a** …, **I want** …, **so that** ….

## Acceptance Criteria
- …

## Tests
Unit:
- `test_<name>` — <logic under test>
Functional:
- `test_<name>` — <end-to-end scenario>

## Key Files
- `src/…` — what changes
```

## Rules

- This skill plans only. It never writes production code — that is `implement-story`.
- Do not write story files until the story set is reviewer-converged.
- Every story must be independently implementable with `test-driven-development`.
- Dependency order is explicit in `TASK.md`.
- A story that generates more than ~6 reviewer findings is too large — split it.
