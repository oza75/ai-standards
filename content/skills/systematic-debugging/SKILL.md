---
name: systematic-debugging
description: Use when encountering any bug, test failure, or unexpected behaviour, before proposing a fix — find the root cause first. Triggers on a failing test, a stack trace, a wrong value, a flaky or intermittent failure, a regression, or any "it works on my machine" surprise. Reproduce as a failing test, isolate, test one hypothesis at a time, and fix the cause rather than the symptom.
---

# systematic-debugging

**The Law:** No fix without a root cause first. Changing code until the symptom
disappears hides the bug; it does not remove it. Find *why* it breaks before you
change anything.

The reason is that a bug is a mismatch between what the code does and what you
believe it does. A fix that lands before you understand the mismatch is a guess;
if the symptom goes away, you have only confirmed that *this* run no longer shows
it, not that the cause is gone. The work below is the cheapest known way to
convert a guess into knowledge — and it is usually faster than guess-and-check,
because every step you take is one you do not have to repeat.

Work the four phases in order. Each one earns the right to start the next: you
cannot analyse a pattern you cannot reproduce, and you cannot test a hypothesis
you have not formed.

## Phase 1 — Root cause investigation

Before proposing any fix, gather evidence:

- **Read the actual error.** The full traceback, the exit code, the real values
  — not the ones you assume. Errors frequently name the cause outright; skipping
  past them to a hunch is how most debugging time gets wasted. Read stack traces
  to the bottom; note line numbers, paths, and codes.
- **Reproduce it reliably first.** Capture the smallest input that triggers the
  failure and turn it into a *failing test*, so the bug is pinned and the
  eventual fix is proven. If you cannot reproduce it, you cannot claim to have
  fixed it — gather more data rather than guessing. Write this test via
  `test-driven-development`; it becomes the regression test in Phase 4.
- **Check recent changes.** What moved that could cause this — a `git diff`, a
  new dependency, a config or environment difference? A bug that appeared today
  usually has a cause from today.
- **Gather evidence at each boundary.** When the failure crosses components
  (CI → build, API → service → database), instrument each boundary to log what
  enters and exits before you theorise. Run once to see *where* it breaks, then
  investigate that component. Read `defense-in-depth.md` for how to think in
  layers.
- **Trace the data flow.** When the error surfaces deep in the call stack, the
  point of failure is rarely the point of origin. Trace the bad value backward
  to where it was created. Read `root-cause-tracing.md` for the technique.

State, in one sentence, the mechanism that produces the wrong result. If you
cannot, you are not done investigating.

## Phase 2 — Pattern analysis

Once you can see the mechanism, place it in context:

- **Find a working example.** Locate similar code in the same codebase that
  behaves correctly. The contrast between working and broken is often the
  fastest path to the difference that matters.
- **Compare completely.** If you are following a reference implementation, read
  it in full rather than skimming — partial understanding reliably reproduces
  the original bug. List *every* difference between working and broken, however
  small; "that can't matter" is a hypothesis, not a fact.
- **Look for the broader class.** Is this an off-by-one repeated across call
  sites, a type or shape mismatch, an unseeded RNG, an async boundary, a mutable
  default? Check whether the same root cause lurks elsewhere before you fix the
  one spot you found.
- **Suspect the dependency, not just your code.** When a library returns or
  behaves differently than you expected, the cause is often a version or API
  mismatch — the signature changed, a default moved, a method was renamed. Re-read
  its current docs with `read-docs` at the project's pinned version before
  assuming the bug is yours. Memory of an old API is a classic false lead.

## Phase 3 — Hypothesis and testing

Now apply the scientific method, one variable at a time:

- **Form one explicit hypothesis.** State it plainly — "I think X is the cause
  because Y" — and predict what you would observe if it were true. A vague
  hunch cannot be tested.
- **Test minimally.** Make the smallest possible change that distinguishes the
  hypothesis from its alternatives, and change *one* variable at a time.
  Simultaneous changes destroy the signal: when the result moves, you will not
  know which change moved it.
- **Decide on evidence, not hope.** Confirmed → Phase 4. Disconfirmed → form a
  new hypothesis; do not stack another fix on top of an unconfirmed one. If you
  do not understand something, say so and investigate rather than pretending.

## Phase 4 — Fix the root cause

- **Write the failing test first** (via `test-driven-development`) if Phase 1
  did not already produce one — the simplest reproduction of the bug. A fix
  without a test that would have caught the bug does not stick.
- **Make a single fix** addressing the cause you confirmed. No "while I'm here"
  refactors bundled in; they obscure whether the fix worked.
- **Verify.** The reproduction test passes, and nothing else broke. Run the full
  gate via `verification-before-completion` — the fix must not break anything
  else. Add a regression test if the existing suite would not have caught this
  bug.
- **If three or more fixes have failed, question the architecture, not the
  hypothesis.** Repeated fixes that each surface a new problem in a different
  place, or that demand ever-larger refactors, are a signal that the design is
  wrong — not that the next patch is the one. Stop and reconsider the structure
  before attempting fix number four.

## Never paper over a symptom

Before you can explain the cause, do not reach for any of these — each one hides
the bug instead of removing it, and the next person (often you) pays for it:

- **Catch-and-ignore** — swallowing the exception so the error stops printing.
- **Blind retry** — looping until it happens to succeed, with no idea why it
  failed.
- **Hard-coded special case** — branching on the one input that breaks, leaving
  the class of inputs broken.

## Red flags — stop and return to Phase 1

If you catch yourself thinking any of these, you have left the process:

- "Quick fix now, investigate later."
- "Just try changing X and see if it works."
- "Add several changes, then run the tests."
- "Skip the test, I'll verify by hand."
- "It's probably X, let me fix that" — before tracing the data flow.
- "I don't fully understand it, but this might work."
- "The reference is long; I'll adapt the pattern from memory."
- "One more fix attempt" — after two or more have already failed.
- Each fix reveals a new problem somewhere else.

The last two mean: question the architecture (Phase 4).

## Common rationalizations

| Excuse | Reality |
|--------|---------|
| "The issue is simple, no need for process." | Simple bugs have root causes too — and the process is fast for them. |
| "Emergency, no time for process." | Systematic debugging is faster than guess-and-check thrashing. |
| "Just try this first, then investigate." | The first fix sets the pattern. Do it right from the start. |
| "I'll write the test after I confirm the fix." | Untested fixes don't stick; a failing test first is what proves the fix. |
| "Multiple fixes at once saves time." | You can't tell which one worked, and you risk new bugs. |
| "The reference is long; I'll adapt it." | Partial understanding reproduces the original bug. Read it fully. |
| "I see the problem, let me fix it." | Seeing the symptom is not understanding the cause. |
| "One more fix attempt." (after 2+ failures) | Three failures point at the architecture, not the next patch. |

## How this fits the other skills

- The reproduction and regression tests are written via
  `test-driven-development` (Phase 1 and Phase 4).
- After the fix, run the full gate via `verification-before-completion`; a fixed
  bug is verified only when the suite is green with the behaviour observed.
- `root-cause-tracing.md` (trace a bug back to its origin) and
  `defense-in-depth.md` (fix at the right layer, then make the bug structurally
  impossible) are the two supporting references in this directory — read them
  when the failure is deep in the stack or crosses component boundaries.

---

_Adapted from [superpowers](https://github.com/obra/superpowers) by Jesse Vincent (MIT License, © 2025), merged with project standards._
