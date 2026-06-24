---
name: review
---

# Code Review

Review the code changes in the current working tree against the active story's acceptance criteria.

## What to check

1. Every acceptance criterion in the story file is satisfied.
2. Every required test from the story file is present and meaningful.
3. `make check` passes (ruff + mypy + pytest).
4. No security issues, correctness bugs, or broken API contracts.

## How to invoke

Open the story file, read the acceptance criteria, then run this prompt.
The `@reviewer` agent will analyse the code and return findings by severity.

## Output

Return findings as:
- **CRITICAL** — blocks merge
- **MAJOR** — blocks merge
- **MINOR** — should fix before merge
- **NIT** — optional cleanup

A clean review has zero CRITICAL and zero MAJOR findings.
