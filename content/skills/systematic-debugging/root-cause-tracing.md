# Root cause tracing

Read this from Phase 1 when the error surfaces deep in the call stack and it is
unclear where the bad value came from.

## The idea

A bug often manifests far from where it was caused — a file written to the wrong
directory, a database opened with the wrong path, a `None` that should have been
a list. The instinct is to fix it where the error appears, but the point of
failure is rarely the point of origin. Patching there treats a symptom and
leaves the real defect free to resurface through another path.

**Trace the bad value backward through the call chain until you find where it
was created, then fix it at the source.**

## When to trace backward

- The error happens deep in execution, not at an entry point.
- The stack trace shows a long call chain.
- It is unclear where the invalid data originated.
- You need to find which test or code path triggers the problem.

If you genuinely cannot trace one level further up (a true dead end), fixing at
the symptom point is acceptable — but treat that as the exception, and add
validation as described in `defense-in-depth.md`.

## The process

Walk one level up at a time, carrying the bad value with you.

1. **Observe the symptom.** Note exactly where and how the error appears.
2. **Find the immediate cause.** What line directly produces the error?
3. **Ask what called this**, with what arguments.
4. **Keep tracing up.** Follow the offending value through each caller. At each
   level ask: was the value already wrong when it arrived here, or did this
   frame corrupt it?
5. **Identify the original trigger** — the first place the value became wrong.
   Fix there.

A worked example. The symptom is `git init` running in the source tree instead
of a temp directory:

```
git init runs in process.cwd()        # symptom: empty cwd resolves to here
  ← WorktreeManager called with projectDir = ''
    ← Session.create() passed the empty string through
      ← test read context.tempDir before the fixture had set it
        ← setupTest() returns { tempDir: '' } until setup runs   # origin
```

The fix belongs at the origin (make `tempDir` raise if read before setup), not
at the `git init` call. Fixing the call site would leave every other consumer of
the empty value still broken.

## When you cannot trace by hand

Add instrumentation that records the call chain at the dangerous operation,
*before* it runs — not after it fails, when the context is already lost. Capture
the value, the surrounding state, and the stack:

```python
import traceback, os, sys

def git_init(directory: str) -> None:
    print(
        f"DEBUG git_init: directory={directory!r} cwd={os.getcwd()!r}",
        file=sys.stderr,
    )
    traceback.print_stack(file=sys.stderr)
    # ... proceed
```

Write to stderr (or `print`), not the application logger — the logger may be
suppressed or buffered during tests, and you need the output to survive. Run,
capture, and read the stack traces: look for the test or call site that appears,
the line that triggers the call, and any repeated parameter.

If a failure appears during a test run but you cannot tell which test causes it,
bisect: run tests in halves until the smallest failing set isolates the culprit.

## Then make it impossible

Finding and fixing the source removes *this* bug. To stop the same class of bug
returning through a different path, add validation at each layer the value passes
through — see `defense-in-depth.md`.
