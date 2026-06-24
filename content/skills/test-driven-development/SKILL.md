---
name: test-driven-development
description: Implement one story strictly test-first — failing test before any production code.
---

# test-driven-development

Implement the current story one acceptance criterion at a time. Never write production code before a failing test exists for it.

## Cycle

1. **Read the story** — understand every acceptance criterion before writing anything.
2. **Write one failing test** — targeting a single criterion. The test must fail because the behaviour does not exist yet, not because of a syntax error.
3. **Watch it fail** — run the test suite and confirm the test fails with the expected message.
4. **Write the minimal code** — only enough to make the failing test pass. No extras, no anticipating the next test.
5. **Watch it pass** — re-run the suite. The new test must pass; no existing test may regress.
6. **Refactor** — improve structure, names, clarity. The suite must stay green throughout.
7. **Repeat** for the next criterion.

## Rules

- Never write production code without a failing test in hand.
- Minimal means minimal — resist the urge to anticipate future tests.
- Refactor only on green, never on red.
- If a test is hard to write, that is a design signal: simplify the interface before writing the test.
- A claim of "tests pass" is only valid when backed by fresh command output.
