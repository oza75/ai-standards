---
name: plan-task
description: Decompose a task into user stories, run the reviewer convergence loop, and write story files.
---

# plan-task

Decompose the given task into user stories following the project's TDD workflow.

## Steps

1. Read `CLAUDE.md` (or equivalent) to understand the project's working agreement.
2. Propose a set of user stories with acceptance criteria and a dependency order.
3. Run the reviewer convergence loop (using the `review` skill or a reviewer agent)
   until no CRITICAL or MAJOR findings remain.
4. Write each converged story as a file under `docs/codes/tasks/<TASK>/user-stories/`.

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

## Notes

- Each story must be independently implementable with a failing-test-first approach.
- Dependency order must be explicit in the task's `TASK.md`.
- Do not start coding until stories are reviewer-converged.
