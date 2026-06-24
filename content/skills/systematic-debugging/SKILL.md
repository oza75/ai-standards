---
name: systematic-debugging
description: Locate root cause before attempting any fix — never apply speculative patches.
---

# systematic-debugging

Never apply a fix before the root cause is understood. Guessing at a fix without knowing the cause creates hidden regressions.

## Steps

1. **Reproduce** — confirm the bug is reliably reproducible. Write a minimal failing test case or command that triggers it.
2. **Isolate** — narrow the failure to the smallest unit: a single function, a single code path, a single interaction.
3. **Hypothesise** — form one specific hypothesis about the cause. Write it down explicitly.
4. **Verify** — use the test suite, logging, or a REPL to confirm or refute the hypothesis. Do not skip this step.
5. **Fix** — apply the fix only after the hypothesis is confirmed. The fix should follow directly from the cause.
6. **Regression test** — add a test that would have caught this bug before the fix lands.

## Rules

- One hypothesis, one fix, one test — never apply multiple speculative fixes at once.
- If the hypothesis is wrong, form a new one and repeat. Do not accumulate speculative changes.
- A "fixed" bug is only verified when a regression test proves it. Write the test before marking the bug closed.
