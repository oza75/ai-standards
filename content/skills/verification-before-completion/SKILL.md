---
name: verification-before-completion
description: Run the full verification gate before marking any story done.
---

# verification-before-completion

No story is marked `done` until the full verification gate passes with fresh output.

## Gate

Run all four checks in order:

```
uv run ruff check .
uv run ruff format --check .
uv run mypy src/
uv run pytest
```

All four must exit 0. A partial pass — tests green but mypy failing — is not a pass.

## Rules

- Run the gate fresh; do not rely on output from an earlier point in the session.
- Fix every failure before marking the story done, however minor.
- Paste the fresh command output to confirm. "All passing" without output is not verified.
- If the gate was green before a late refactor, run it again after.
