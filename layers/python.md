# Python AI Coding Standards

Python-specific standards. Applied in addition to `universal.md`.

## Typing

- All public functions and methods have full type annotations (params + return).
- Use `from __future__ import annotations` in Python < 3.10 for forward refs.
- Prefer `X | None` over `Optional[X]`; prefer `X | Y` over `Union[X, Y]`.
- No `Any` in public interfaces; use `Any` only when integration-layer types
  force it (e.g. third-party callbacks), and annotate the variable explicitly.
- Run `mypy --strict` as part of `make check`; zero tolerance for type errors.

## Async-Sync

- Do not mix sync and async in the same function.
- Pure business logic is sync; I/O boundaries are async.
- Never call `asyncio.run()` inside a function that might itself be running in
  an event loop — use `await` instead.
- Mark async helpers with `async def`; never use `asyncio.get_event_loop()`.

## Tools

- Package management: `uv`. Never commit a virtualenv.
- Linting/formatting: `ruff check` + `ruff format`.
- Type checking: `mypy --strict`.
- Testing: `pytest`. No `unittest.TestCase` subclasses.
- `make check` runs ruff + mypy + pytest in that order; all must pass before commit.
