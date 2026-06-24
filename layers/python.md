# Python AI Coding Standards

Python-specific standards. Applied in addition to `universal.md`.

## Typing

Every function and method signature is fully typed — arguments and return type. Prefer
precise types (`Sequence[str]`, `dict[str, int]`, a dataclass, an `Enum`) over `Any`.
`mypy --strict` must pass.

- `Any` in public interfaces is not acceptable. Use it only when an integration boundary
  forces it (e.g. a third-party callback), and annotate the variable explicitly.
- Prefer `X | None` over `Optional[X]`; prefer `X | Y` over `Union[X, Y]`.

## The _ Prefix

Python does not enforce privacy, so a leading `_` is usually noise. Use it only for:

- A genuinely unused throwaway: `for _ in range(n)`, `name, _ = pair`.
- Real `__name` mangling when subclass collision is a concrete risk.

Module-level `_helper` "privacy" is not a reason. If it should not be part of the public
API, that is a module-boundary question, not a naming question.

## Async-Sync

Async is for **I/O-bound** work: concurrent API calls, dataset downloads, network
fan-outs. Use it there — overlapping network waits is real throughput.

CPU-bound code and computation-bound work stay **synchronous**. Their parallelism comes
from vectorisation, multiprocessing, or worker pools — not asyncio, which cannot
parallelise CPU under the GIL.

- Do not mix sync and async in the same function.
- Never call `asyncio.run()` inside a function that might itself be running in an event
  loop — use `await` instead.
- Mark async helpers with `async def`; never use `asyncio.get_event_loop()`.

## Tools

- Package management: `uv`. Never commit a virtualenv.
- Linting / formatting: `ruff check` + `ruff format`.
- Type checking: `mypy --strict`.
- Testing: `pytest`. No `unittest.TestCase` subclasses.

The verification gate — all four must pass before a story is done:

```
uv run ruff check .
uv run ruff format --check .
uv run mypy src/
uv run pytest
```

A claim of success is backed by fresh command output, never by assumption.
