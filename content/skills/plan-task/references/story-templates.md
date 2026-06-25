# Story file templates

The file formats for Phase 5 — written only after the story set is
reviewer-converged. Two files: one `TASK.md` for the task, one file per story
under `user-stories/`.

## TASK.md

Path: `docs/codes/tasks/[CODE]-[short-name]/TASK.md`

```markdown
# [CODE] · [Title]

## Context
<why this task exists, current state, goal, constraints>

## User Stories
- [[CODE]-1 — Title](user-stories/[CODE]-1-[name].md)
- …
```

The story list doubles as the dependency map — order it so each story's
predecessors come before it, and call out any parallelism explicitly (e.g.
"STD-1 ∥ STD-2"). A reader should be able to pick the next implementable story
from this list alone.

## Per-story file

Path: `docs/codes/tasks/[CODE]-[short-name]/user-stories/[CODE]-[N]-[short].md`

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

The **Tests** section is part of the specification, not an afterthought — the
story is built test-first, so its test list is what `implement-story` turns into
failing tests before any code exists. List both unit tests (the logic in
isolation) and functional tests (the end-to-end behaviour the acceptance
criteria describe).
