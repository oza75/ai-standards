---
name: review
description: Run a convergence-loop code review using an opus-class reviewer until no CRITICAL or MAJOR findings remain.
---

# review

Run a strict code review against the acceptance criteria for the current story.
Loop until convergence: no CRITICAL or MAJOR findings in two consecutive passes.

## Reviewer instructions

You are reviewing code for the story currently in scope.

1. Read the story file to get acceptance criteria and required tests.
2. Review the implementation against every criterion.
3. Flag findings as **CRITICAL**, **MAJOR**, **MINOR**, or **NIT**.
4. Return all findings with a clear verdict: PASS (no CRITICAL/MAJOR) or CHANGES REQUIRED.

## Severity definitions

| Level | Definition |
|-------|-----------|
| CRITICAL | Acceptance criterion not met; correctness broken; security issue |
| MAJOR | Test coverage gap for a required test; significant design flaw |
| MINOR | Robustness or maintainability issue that could cause future bugs |
| NIT | Style, naming, or cosmetic issue with a clear fix |

## Convergence rule

The loop stops when a reviewer pass returns PASS. Run at least one more pass after
the first PASS to confirm convergence — a single clean pass can be a fluke.
Stop when two consecutive passes return no CRITICAL or MAJOR findings.

## Notes

- Always use an opus-class model (claude-opus-4-8) for reviewer agents.
- Do not stop early to save tokens — a false PASS is worse than a slow review.
