# Defense in depth

Read this from Phase 1 when a failure crosses component boundaries, and again in
Phase 4 once you have found the root cause and want to make the bug structurally
impossible rather than merely fixed.

## The idea

When a bug comes from invalid data, adding one check where you noticed it feels
like enough. But a single checkpoint is easy to bypass — a different code path, a
later refactor, a mock in a test — and the bug returns. Validating at each layer
the data passes through turns "we fixed the bug" into "the bug cannot happen",
because each layer catches the cases the others miss.

This is not a licence to skip Phase 1. Fix the root cause first; the layers are
what keep it fixed.

## The four layers

Each layer answers a different question, so each catches a different failure.

**Layer 1 — entry-point validation.** Reject obviously invalid input at the API
boundary: empty values, missing files, wrong types. This stops the largest share
of bad data before it travels anywhere.

```python
def create_project(name: str, working_directory: str) -> Project:
    if not working_directory.strip():
        raise ValueError("working_directory cannot be empty")
    if not os.path.isdir(working_directory):
        raise ValueError(f"working_directory is not a directory: {working_directory}")
    # ... proceed
```

**Layer 2 — business-logic validation.** Even valid-looking input can be wrong
for *this* operation. Check that the data makes sense for what you are about to
do. This catches edge cases and the paths that bypassed Layer 1 (for example, a
mock that constructed the object directly).

```python
def initialize_workspace(project_dir: str, session_id: str) -> None:
    if not project_dir:
        raise ValueError("project_dir required for workspace initialization")
    # ... proceed
```

**Layer 3 — environment guards.** Refuse operations that are dangerous in a
particular context. The classic case: during tests, refuse a destructive
operation anywhere outside a temp directory, so a stray empty path can never
touch the real tree.

```python
def git_init(directory: str) -> None:
    if os.environ.get("PYTEST_CURRENT_TEST"):
        resolved = os.path.realpath(directory)
        if not resolved.startswith(os.path.realpath(tempfile.gettempdir())):
            raise RuntimeError(f"refusing git init outside temp dir during tests: {directory}")
    # ... proceed
```

**Layer 4 — debug instrumentation.** When the other layers somehow let something
through, captured context is what lets you diagnose it. Log the value, the
surrounding state, and the call stack before the dangerous operation. See
`root-cause-tracing.md` for the logging pattern.

## Applying the pattern

After you have found the root cause:

1. **Trace the data flow** — where the bad value originates and everywhere it is
   used (`root-cause-tracing.md`).
2. **Map the checkpoints** — list every point the data passes through.
3. **Add validation at each layer** — entry, business, environment, debug.
4. **Test each layer independently** — deliberately bypass Layer 1 and confirm
   Layer 2 still catches the problem, and so on. A layer you have not seen catch
   anything is a layer you cannot rely on.

## Why all four

In real incidents, each layer earns its place by catching what the others let
slip: different code paths bypass entry validation, mocks bypass business-logic
checks, platform edge cases need the environment guard, and the debug logging is
what finally explains the structural misuse. Do not stop at one validation point.
