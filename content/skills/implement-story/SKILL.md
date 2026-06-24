---
name: implement-story
description: Use to build a planned user story — the coding loop that takes one story through TDD, the verification gate, and review to done. Run after plan-task; repeat per story in dependency order.
---

# implement-story

The **implementation** half of the lifecycle: take a reviewer-converged story
(from `plan-task`) and build it. This is the coding loop, run **one story at a
time, in dependency order**. It nests `test-driven-development`,
`verification-before-completion`, `reviewer-loop`, and `systematic-debugging`.

Never bulk-implement; never write code on the fly or half-finished. If the story
is not yet planned and reviewer-converged, stop and run `plan-task` first.

## The loop — per story

1. **Start the story.** Branch `<type>/[CODE]-[N]-[short]`; set the story's
   `status: progress`. Re-read its acceptance criteria and test list.

2. **Build it test-first.** Run `test-driven-development`: for each acceptance
   criterion, write one failing test → watch it fail for the right reason →
   minimal code to pass → refactor on green. One unit at a time, never a batch
   with tests back-filled.

3. **Debug systematically when needed.** If a test fails for a non-obvious
   reason, switch to `systematic-debugging` — root cause before any fix — then
   return to the loop.

4. **Verify.** Run `verification-before-completion`: the full gate green in a
   single fresh run **and** the behaviour observed (the functional test, or a
   real run of the feature). A partial pass is not done.

5. **Review to convergence.** Run `reviewer-loop` on the code — delegating each
   pass to the `code-reviewer` subagent — until no CRITICAL or MAJOR findings
   remain. Address every blocking finding.

6. **Finish.** Set `status: done`, `completed: <datetime>`; commit with a
   Conventional Commit referencing the story code; merge.

7. **Next story.** Repeat for the next story whose dependencies are now done.

## Rules

- One story at a time; one unit at a time within a story.
- No production code without a failing test first (`test-driven-development`).
- A story is done only when the gate is green and the review has converged —
  both, freshly verified, not assumed.
- Respect the dependency order from the task's `TASK.md`; do not start a story
  whose predecessors are not done.
- If, mid-implementation, a story turns out to be mis-scoped, stop and return to
  `plan-task` rather than improvising a larger change.
