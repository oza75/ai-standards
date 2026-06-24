---
name: test-driven-development
description: Implement one unit of behaviour at a time, strictly test-first — a failing test you watched fail before any production code exists for it.
---

# test-driven-development

**The Law:** Write the test first, watch it fail, then write the minimal code
to pass. If you did not watch the test fail, you do not know that it tests the
right thing — a test that has never been red proves nothing.

This applies to every change: new features, bug fixes, refactors that change
behaviour. No exceptions.

## The cycle — one small unit of behaviour at a time

1. **RED — write one failing test.**
   Express the next required behaviour as a single test. Arrange–Act–Assert
   with a blank line between the three segments; a docstring stating the logic
   under test (the scenario and expected behaviour, not a description of the
   code); an intent-revealing name (`test_already_correct_input_is_left_unchanged`,
   not `test_1`). Match rigor to the surface: deterministic logic gets a strict
   assertion on the output; nondeterministic surfaces get pinned on mechanics
   and invariants — shapes, round-trips, seeded reproducibility — not exact
   values.

2. **Watch it fail, for the right reason.**
   Run the test. Confirm it fails *because the behaviour is missing* — not
   because of an import error, a typo in the test, or a fixture problem. A
   failure you did not read is not a failure you can trust.

3. **GREEN — minimal code to pass.**
   Write the least code that makes the test pass: no extra features, no
   speculative generality, no anticipating the next test. Run the suite;
   confirm green and that no existing test regressed.

4. **REFACTOR — clean up while green.**
   Improve names, structure, and duplication with the suite staying green
   throughout. Docstrings and comments come in a later second pass, per the
   standard — never narrated as you go.

5. **Repeat** for the next unit.

## Rules

- **No production code before a failing test exists for it.** If you wrote it
  first, delete it and start from the test. This is not negotiable.
- Implement **one unit at a time.** Never write a batch of code and back-fill
  tests against it.
- Refactor only on green, never on red.
- If a test is hard to write, that is a design signal — simplify the interface
  before writing the test, do not write a contorted test around a bad shape.
- A claim of "tests pass" is valid only when backed by fresh command output.

## Rationalizations to reject

- *"I'll add the test after — the code is obvious."* Then the test is shaped to
  the code, not the behaviour, and you never saw it fail. Write it first.
- *"I verified it by hand / in the REPL."* Manual checks are not repeatable and
  guard no regression. Encode it as a test.
- *"I already wrote the implementation; deleting it feels wasteful."* Sunk cost.
  Untested code is a liability, not an asset. Reset to the test.

When the unit is complete, hand off to `verification-before-completion` before
claiming the story is done.
