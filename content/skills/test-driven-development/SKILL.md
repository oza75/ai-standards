---
name: test-driven-development
description: Use when implementing any feature, bugfix, or behaviour change — write a failing test first, watch it fail for the right reason, then the minimal code to pass. Triggers on "implement", "add", "fix", "build", "change the behaviour of", or whenever production code is about to be written for a unit that has no failing test yet.
---

# test-driven-development

**The Law:** Write the test first, watch it fail, then write the minimal code
to pass. If you did not watch the test fail, you do not know that it tests the
right thing — a test that has never been red proves nothing.

This applies to every change: new features, bug fixes, refactors that change
behaviour. No exceptions.

The reason the order is fixed is that a test written *after* the code is shaped
by the code you already have — it asserts what you built, not what the behaviour
requires, and it has never demonstrated that it can catch a regression. Watching
it fail first is the only proof the test is wired to the behaviour at all.

## The cycle — one small unit of behaviour at a time

Work one unit at a time. Each unit goes RED → verify red → GREEN → verify green
→ REFACTOR, then on to the next. Never write a batch of code and back-fill tests
against it.

### 1. RED — write one failing test

Express the next required behaviour as a single test. The shape that makes a
test readable a year from now:

- **Arrange–Act–Assert**, with a blank line separating the three segments, so
  the setup, the action, and the check are visually distinct.
- A **multi-line docstring** stating the *logic under test* — the scenario and
  the expected behaviour, not a description of the code. (Opening `"""` on its
  own line, content indented, closing `"""` on its own line.)
- An **intent-revealing name** that states the scenario:
  `test_already_correct_input_is_left_unchanged`, not `test_1`.

**Match rigor to the surface.** Test what can actually break:

- Fully deterministic logic gets a strict assertion on the exact output.
- Nondeterministic or hard-to-pin surfaces (sampling, model output, timing,
  generated IDs) are tested for **mechanics and invariants** — shapes,
  round-trips, seeded reproducibility, ordering, bounds — not exact values.

**Value over coverage.** Test behaviour that can break and matters. Do not
assert the framework itself, or facts that are trivially true regardless of your
code — those add maintenance cost and catch nothing.

If the test is hard to write, that is a design signal. Hard to test usually
means hard to use — simplify the interface before writing the test, rather than
contorting the test around an awkward shape.

```python
def test_retries_until_the_operation_succeeds():
    """
    A flaky operation that fails twice then succeeds should be retried
    until it returns, and the caller should receive the successful result.
    """
    attempts = {"count": 0}

    def operation():
        attempts["count"] += 1
        if attempts["count"] < 3:
            raise RuntimeError("transient failure")
        return "ok"

    result = retry_operation(operation)

    assert result == "ok"
    assert attempts["count"] == 3
```

Contrast with a test that asserts on a mock instead of behaviour — it passes
when the mock is wired up and tells you nothing about whether the real code
retries. See [testing-anti-patterns.md](testing-anti-patterns.md).

### 2. Verify RED — watch it fail, for the right reason

Run the test. Confirm it fails *because the behaviour is missing* — not because
of an import error, a typo in the test, or a broken fixture. A failure you did
not read is not a failure you can trust.

- Test **fails** (not errors out)? Read the message — is it the assertion you
  expected, or something incidental?
- Test **passes** already? Then it is testing existing behaviour, not the new
  thing. Fix the test.
- Test **errors** (import, fixture, syntax)? Fix the error and re-run until it
  fails for the right reason.

This step is not optional. It is the only point at which you observe that the
test is connected to the behaviour.

### 3. GREEN — minimal code to pass

Write the least code that makes the test pass: no extra features, no speculative
generality, no anticipating the next test. Resist the urge to add the options,
config flags, or edge-case handling you "know you'll need" — they belong to
their own future tests.

### 4. Verify GREEN — watch it pass, output pristine

Run the suite. Confirm:

- The new test passes.
- No existing test regressed.
- The output is **pristine** — no new warnings, no stray prints, no deprecation
  noise. Warnings you let through now are warnings you stop reading later.

If the new test fails, fix the code, not the test. If another test broke, fix it
before moving on.

A claim of "tests pass" is valid only when backed by fresh command output.

### 5. REFACTOR — clean up while green

Improve names, remove duplication, extract helpers — with the suite staying
green throughout. Refactor only on green, never on red.

Docstrings and comments for the production code come in a **later, separate
pass**, per the project Docs standard — never narrated as you write the code.
Writing code and prose at once produces narration that drifts from the code.

### 6. Repeat for the next unit.

## Rules

- **No production code before a failing test exists for it.** If you wrote it
  first, delete it and start from the test. Keeping it "as a reference" is
  testing-after in disguise — you will shape the test to the code you kept.
- Implement **one unit at a time.** Never write a batch of code and back-fill
  tests against it.
- Refactor only on green, never on red.
- Tests use **real code**; reach for mocks only when a dependency is genuinely
  unavoidable (slow, external, nondeterministic), and never assert on the mock
  itself.
- A bug fix starts with a **failing test that reproduces the bug.** The test
  proves the fix and guards against regression. (If the failure reason is not
  obvious, hand off to `systematic-debugging` for root cause first.)

## Rationalizations to reject

| Excuse | Reality |
|--------|---------|
| "I'll add the test after — the code is obvious." | Then the test is shaped to the code, not the behaviour, and you never saw it fail. Write it first. |
| "I verified it by hand / in the REPL." | Manual checks are not repeatable and guard no regression. Encode it as a test. |
| "I already wrote the implementation; deleting it feels wasteful." | Sunk cost. Untested code is a liability, not an asset. Reset to the test. |
| "Too simple to test." | Simple code still breaks, and the test costs seconds. If it is worth writing, it is worth a test. |
| "Tests-after achieve the same goal." | Tests-after answer "what does this do?"; tests-first answer "what should this do?" Only the second discovers the edge cases you forgot. |
| "I need to explore first." | Fine — explore freely, then throw the exploration away and start the unit with TDD. |

## Red flags — stop and start over

If any of these is true, the unit is not being built test-first. Reset to a
failing test:

- Production code was written before its test.
- A test passed the first time you ran it (it never went red).
- You cannot explain *why* the test failed in the RED step.
- Tests are being "added later", after the implementation is done.
- You are reasoning "just this once" or "this case is different because…".
- A test asserts on a mock's behaviour rather than the code's.

## Verification checklist

Before handing the unit off, confirm:

- [ ] Every new function or method has a test.
- [ ] You watched each test fail before implementing it.
- [ ] Each test failed for the expected reason (behaviour missing, not a typo).
- [ ] You wrote the minimal code to pass.
- [ ] All tests pass and no existing test regressed.
- [ ] Output is pristine — no new warnings or noise.
- [ ] Tests exercise real code; mocks only where unavoidable, never asserted on.
- [ ] The test name and docstring state the scenario, not the implementation.

If you cannot check every box, the unit was not built test-first — start over.

## Where tests live, and what comes next

Unit tests for isolated logic go in `tests/unit/`; functional tests for
end-to-end scenarios go in `tests/functional/`.

When the unit is complete, hand off to `verification-before-completion` before
claiming the story is done — the full gate (lint, format, types, the whole test
suite) must pass with the behaviour observed, not assumed.

For mocking and test-utility pitfalls — testing what the mocks do instead of
what the code does, test-only methods leaking into production, incomplete mocks
— read [testing-anti-patterns.md](testing-anti-patterns.md) whenever you add a
mock or a test helper.

---

_Adapted from [superpowers](https://github.com/obra/superpowers) by Jesse Vincent (MIT License, © 2025), merged with project standards._
