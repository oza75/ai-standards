---
name: reviewer-loop
description: Run iterative code review with claude-opus-4-8 until no CRITICAL or MAJOR findings remain.
---

# reviewer-loop

Run review passes with **claude-opus-4-8** until convergence: no CRITICAL or MAJOR findings in a full pass.

## Steps

1. Run a review pass — share the story's acceptance criteria and the implementation in scope.
2. Receive findings categorised as CRITICAL, MAJOR, MINOR, or NIT.
3. If any CRITICAL or MAJOR findings exist: fix every one of them, then return to step 1.
4. When a full pass returns no CRITICAL or MAJOR findings: the loop converges.

## Severity levels

| Level | Blocks? | Definition |
|-------|---------|-----------|
| CRITICAL | Yes | Acceptance criterion unmet; correctness broken; security issue |
| MAJOR | Yes | Required test missing; significant design flaw; API contract violated |
| MINOR | No | Robustness issue that could cause future bugs |
| NIT | No | Style or cosmetic issue with a clear one-line fix |

## Rules

- Always use **claude-opus-4-8** (or better). Never use a smaller model for review.
- MINOR and NIT findings are fix-or-note, not blocking. CRITICAL and MAJOR always block.
- Do not stop early — a single clean pass can be a fluke; loop until the pass is genuinely clean.
- Feed the reviewer both the acceptance criteria and the implementation.
