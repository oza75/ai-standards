---
name: plan-task
description: Turn a goal into shipped, tested code — decompose into reviewer-converged user stories, then implement story by story. The master process that nests the other skills.
---

# plan-task

The master process for turning a goal into shipped, tested code. Every task is
decomposed into **user stories** and built **test-first**. This skill nests
`test-driven-development`, `systematic-debugging`, `verification-before-completion`,
and `reviewer-loop`. Never bulk-implement; never write code on the fly or
half-finished.

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

## Phase 7 — Implement story by story

For each story, in dependency order:

1. Branch `<type>/[CODE]-[N]-[short]`; set the story `status: progress`.
2. Run `test-driven-development`: write the story's tests (red, watched to
   fail) → minimal code to green → refactor — one unit at a time, never bulk.
3. Run `verification-before-completion`: the full gate green **and** the
   behaviour observed.
4. Run `reviewer-loop` on the **code**; address CRITICAL/MAJOR to convergence.
5. Set `status: done`, `completed: <datetime>`; commit (Conventional Commits,
   referencing the story code); merge.

Use `systematic-debugging` whenever a test fails for a non-obvious reason.

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

- Do not start coding until the stories are reviewer-converged.
- Every story must be independently implementable with `test-driven-development`.
- Dependency order is explicit in `TASK.md`.
- A story that generates more than ~6 reviewer findings is too large — split it.
