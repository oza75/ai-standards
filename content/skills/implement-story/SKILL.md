---
name: implement-story
description: Use to build a planned, reviewer-converged user story — the coding loop that takes one story through TDD, the verification gate, and review to done. Run after plan-task; repeat per story in dependency order. Trigger whenever the user is ready to start coding a story, asks to "implement", "build", or "work on" a story, or picks the next story off a task plan — even if they don't name this skill.
---

# implement-story

The **implementation** half of the lifecycle: take a reviewer-converged story
(from `plan-task`) and build it. This is the coding loop, run **one story at a
time, in dependency order**. It nests `test-driven-development`,
`systematic-debugging`, `verification-before-completion`, and `reviewer-loop`.

If the story is not yet planned and reviewer-converged, stop and run `plan-task`
first — building from an unconverged story just bakes in the gaps the planning
loop exists to catch. Never bulk-implement, and never write code on the fly or
leave it half-finished: the discipline below is what keeps each story shippable
on its own.

## The loop — per story

1. **Start the story.** Branch `<type>/[CODE]-[N]-[short]`; set the story's
   `status: progress`. Re-read its acceptance criteria and test list so you build
   to the spec, not to memory.

2. **Build it test-first.** Run `test-driven-development`: for each acceptance
   criterion, write one failing test → watch it fail for the right reason →
   minimal code to pass → refactor on green. Work one unit at a time. Batching the
   code and back-filling tests afterward defeats the point — the failing test is
   what proves the code is wired up and the assertion actually bites. Before
   writing against an external library or API, use `read-docs` to pull its
   current, version-correct docs — write to the real API, not to memory.

3. **Debug systematically when needed.** When a test fails for a non-obvious
   reason, switch to `systematic-debugging` and find the root cause before any
   fix, then return to the loop. A patch that makes the symptom disappear without
   explaining it tends to resurface.

4. **Verify.** Run `verification-before-completion`: the full gate green in a
   single fresh run **and** the behaviour observed (the functional test, or a real
   run of the feature). A partial or remembered pass is not done.

5. **Review to convergence.** Run `reviewer-loop` on the code, delegating each
   pass to the `reviewer` subagent, until no CRITICAL or MAJOR findings remain.
   Address every blocking finding before moving on.

6. **Finish.** Set `status: done`, `completed: <datetime>`; commit with a
   Conventional Commit referencing the story code; merge.

7. **Next story.** Move to the next story whose dependencies are now done, and
   start the loop again.

## Rules

- One story at a time; one unit at a time within a story.
- No production code without a failing test first (`test-driven-development`).
- A story is done only when the gate is green **and** the review has converged —
  both, freshly verified, not assumed.
- Respect the dependency order from the task's `TASK.md`; do not start a story
  whose predecessors are not done.
- If, mid-implementation, a story turns out to be mis-scoped, stop and return to
  `plan-task` rather than improvising a larger change. Re-planning keeps the work
  reviewable; scope creep inside a story does not.
