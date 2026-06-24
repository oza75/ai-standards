---
name: verification-before-completion
description: No completion claim without fresh verification evidence — run the proof command now and read its full output before saying anything works.
---

# verification-before-completion

**The Law:** No completion claim without fresh verification evidence. "Done",
"passing", "fixed", "it works", "the regression is gone" — each requires a
command you ran **in the current step** whose output supports the claim.
Confidence is not evidence.

## The gate — before stating something works

1. **Identify the proof command.** The exact command whose output confirms the
   claim. For a story, that is the project's full verification gate. For a bug
   fix, the reproduction case now passing plus the full gate.

2. **Run it fresh, now.** Not a remembered run from earlier in the session. If
   anything changed since the last run — even a one-line refactor — the earlier
   output is stale.

3. **Read the full output and the exit code.** The whole thing, not the first
   line. A suite that prints progress dots can still end in a failure summary.

4. **Check the claim against the evidence.** Does the output actually support
   what you are about to say? A green linter is not a passing test suite. A
   passing unit test is not a working end-to-end flow. Do not treat one signal
   as another.

5. **State the result with the evidence attached** — what you ran and what it
   showed.

## The verification gate

The gate is the set of checks that all pass, in a single fresh run, before a
story is done. The concrete commands live in your language layer. For a Python
project that is:

```
uv run ruff check .          # lint
uv run ruff format --check . # formatting
uv run mypy src/             # types (strict)
uv run pytest                # tests
```

All must exit 0. A partial pass — tests green but mypy failing — is not a pass.

## What this blocks

- Claiming success because the code "should" work, or worked before.
- Treating one signal as another: a clean `ruff`/`mypy` run is not proof the
  tests pass; a successful build is not proof of behaviour.
- Trusting a subagent's or tool's "done" without re-running the proof yourself.

## Done means

A story is done when, in a single fresh run, the full gate is green **and** the
behaviour has been observed — the functional test passing, or a real run of the
feature. Only then mark the story `done` and commit.
