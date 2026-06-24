---
name: systematic-debugging
description: Find the root cause before changing any code — reproduce, isolate, test one hypothesis at a time, fix the cause not the symptom.
---

# systematic-debugging

**The Law:** No fix without a root cause first. Changing code until the symptom
disappears hides the bug; it does not remove it. Find *why* it breaks before you
change anything.

## Phase 1 — Reproduce and investigate

- **Reproduce it reliably first.** Capture the smallest input that triggers the
  failure and turn it into a failing test, so the bug is pinned and the eventual
  fix is proven. If you cannot reproduce it, you cannot claim to have fixed it.
- **Read the actual evidence** — the full traceback, the exit code, the real
  values — not the ones you assume. Use `-x -s`, a debugger, or a temporary
  print to observe the real state at the point of failure.
- **Locate where expected and actual diverge.** State, in one sentence, the
  mechanism that produces the wrong result.

## Phase 2 — Pattern analysis

Is this an instance of a broader class — an off-by-one repeated across call
sites, a type/shape mismatch, an unseeded RNG, an async boundary, a mutable
default? Check whether the same root cause lurks elsewhere before you fix the
one spot you found.

## Phase 3 — Hypothesis testing

- Form **one** explicit hypothesis about the cause, and predict what you would
  observe if it were true.
- Test it by changing **one variable at a time** and reading the result. Keep or
  discard the hypothesis on evidence, not hope. Repeat until the cause is
  confirmed. Simultaneous changes destroy the signal.

## Phase 4 — Fix the root cause

- Fix the cause, not the symptom. The reproduction test from Phase 1 must now
  pass.
- Add a regression test if the existing suite would not have caught this bug.
- Run the full verification gate (`verification-before-completion`); the fix must
  not break anything else.

## Rules

- Never paper over a symptom — catch-and-ignore, blind retry, a hard-coded
  special case — before you can explain the cause.
- One change at a time while diagnosing.
- A "fixed" bug is verified only when a regression test proves it. Write that
  test before marking the bug closed.
