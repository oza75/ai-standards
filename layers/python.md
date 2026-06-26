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

## Concurrency & parallelism

Match the tool to the bottleneck. The GIL means threads do not parallelise pure-Python CPU
work — pick the wrong mechanism and you get all the complexity of concurrency with none of
the speedup.

- **I/O-bound** (network, disk, API fan-out): overlap the waits. Use `asyncio` for
  natively-async libraries, or a `ThreadPoolExecutor` (`concurrent.futures`) to run
  blocking I/O calls concurrently. Overlapping network waits is real throughput.
- **CPU-bound** (computation, encoding, heavy transforms): parallelise with a
  `ProcessPoolExecutor` / `multiprocessing`, or push the work into vectorised libraries
  (NumPy, pandas, PyTorch) that release the GIL and run in native code. Never reach for
  asyncio or threads to speed up CPU work.
- Size pools deliberately and reuse them; do not spawn an unbounded number of workers per
  call. Prefer `concurrent.futures` executors with `as_completed` over hand-rolled
  thread/process management.

### Async hygiene

- Do not mix sync and async in the same function.
- Never call `asyncio.run()` inside a function that might itself be running in an event
  loop — use `await` instead.
- Mark async helpers with `async def`; never use `asyncio.get_event_loop()`.

## Performance & memory

- Stream large data with **generators and iterators**; do not build a full list when you
  consume it once. Process in chunks rather than loading everything into memory.
- Reach for the right structure: `set` / `dict` for membership and lookup instead of a
  linear scan over a list, `collections.deque` for queues, `__slots__` on small objects
  created in large numbers.
- Prefer vectorised array operations over element-wise Python loops for numeric work.
- Profile a hot path with real data (`cProfile`, `timeit`) before optimising it — but
  write the obviously-efficient form first rather than the naive one and tuning later.

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
