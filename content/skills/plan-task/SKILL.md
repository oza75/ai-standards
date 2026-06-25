---
name: plan-task
description: Use before any code is written — decompose a goal into reviewer-converged user stories and write the story files. Trigger whenever the user wants to plan a task, break work into stories, scope a feature, or asks "how should we approach this?" — even if they don't name this skill. Planning only; hand off to implement-story to build them.
---

# plan-task

The **planning** half of the lifecycle: turn a goal into a reviewer-converged set
of written user stories, each built to be implemented test-first.

This skill stops at a plan. It never writes production code — that is
`implement-story`. Keeping planning and building separate is the whole point: a
plan settled and reviewed on its own terms produces better stories than one
improvised while coding. When the stories are converged and written, hand off to
`implement-story`.

Planning is a **loop**: propose → review → revise, until the decomposition
converges. Write no story files — and no code — before the story set converges.
Files written too early just get rewritten when the decomposition shifts.

## Phase 1 — Scope

State the task outcome, why it exists, and its constraints, sourced from the
project roadmap or the request. Assign a short task code and a kebab name, giving
the folder `docs/codes/tasks/[CODE]-[short-name]/`.

## Phase 2 — Explore

Find existing code, patterns, and utilities to reuse **before** proposing
anything new — a plan that ignores what is already there proposes redundant work.
Note what must stay untouched: invariants, guardrails, data that must not be
modified.

When the task involves an external library, framework, or API, use `read-docs`
to pull its **current** documentation now — before you propose an approach. A
plan built on a remembered (and possibly outdated or version-wrong) API bakes in
work that will not survive contact with the real library.

## Phase 3 — Propose the story set (no files yet)

Draft the candidate stories: title, a one-line "As a / I want / so that", the
rough tests each implies, and dependencies. Aim for INVEST stories —
independent, negotiable, valuable, estimable, small, testable. This is a
proposal to be challenged, so keep it cheap to change; no files yet.

## Phase 4 — Reviewer gate #1 (the story set)

Hand the decomposition to `reviewer-loop`. Challenge the **choice and
boundaries**, not the prose: missing or redundant stories, wrong sizing,
untestable stories, mis-ordered dependencies, coverage gaps. **Loop — revise and
re-review — until it converges** (no CRITICAL/MAJOR). **Write no files before
this converges**, because the file structure mirrors the decomposition and the
decomposition is still moving.

## Phase 5 — Write the task and stories

Now that the set is settled, write `TASK.md` and one file per story. Every story
carries its **test list** (unit + functional) — the tests are part of the
specification because the work is built test-first.

For the exact file formats, see `references/story-templates.md`.

## Phase 6 — Reviewer gate #2 (the written stories)

Run `reviewer-loop` again, this time on the written artifacts — acceptance
criteria, test lists, key files, checked against the project's standards. Gate #1
validated the shape of the decomposition; this one validates that each written
story is complete and faithful. Loop to convergence.

## Done — hand off to implementation

Planning is complete when the stories are written and reviewer-converged. Do
**not** start coding here. Hand off to `implement-story`, which takes the stories
one at a time through the coding loop (TDD → verification → review → commit).

## Rules

- This skill plans only. It never writes production code — that is `implement-story`.
- Do not write story files until the story set is reviewer-converged.
- Every story must be independently implementable with `test-driven-development`.
- Dependency order is explicit in `TASK.md`.
- A story that generates more than ~6 reviewer findings is too large — split it.
