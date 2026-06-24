---
name: review
description: Run one strict code review pass against the active story's acceptance criteria.
---

# review

Run a single review pass for the story currently in scope. Use this skill inside `reviewer-loop` — do not call it in isolation when iterating toward convergence.

## What to review

1. Every acceptance criterion in the story file is explicitly satisfied.
2. Every required test from the story file is present, meaningful, and not trivially true.
3. The verification gate (`make check`) passes.
4. No correctness bugs, security issues, or broken API contracts.
5. No dead code, leaked state, or hardcoded values that belong in configuration.

## Severity levels

| Level | Blocks merge? | Definition |
|-------|-------------|-----------|
| CRITICAL | Yes | Acceptance criterion unmet; correctness broken; security issue |
| MAJOR | Yes | Required test missing; significant design flaw; API contract broken |
| MINOR | No | Robustness or maintainability issue that could cause future bugs |
| NIT | No | Style, naming, or cosmetic issue with a clear one-line fix |

## Output format

```
## Verdict: PASS | CHANGES REQUIRED

### CRITICAL
- <finding>

### MAJOR
- <finding>

### MINOR / NIT
- <finding>
```

## Rules

- Read code and tests — do not edit anything.
- Check every acceptance criterion explicitly — do not assume satisfaction.
- If uncertain whether an issue is CRITICAL or MAJOR, escalate to the higher severity.
- Always use **claude-opus-4-8** (or better). Never downgrade the review model.
