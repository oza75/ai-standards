---
name: verification-before-completion
description: Use before claiming any work is complete, fixed, or passing, and before committing. "Done", "passing", "fixed", "it works", "the regression is gone" each require a command you ran in the current step whose output supports the claim — run the verification gate fresh and read its full output first.
---

# verification-before-completion

**The Law:** No completion claim without fresh verification evidence. "Done",
"passing", "fixed", "it works", "the regression is gone" — each requires a
command you ran **in the current step** whose output supports the claim.
Confidence is not evidence.

The reason is simple: a claim of success is a claim about the present state of
the code. Anything you remember from earlier in the session describes a past
state that may no longer hold. The only way to know the current state is to run
the proof now and read what it says.

## The gate — before stating something works

1. **Identify the proof command.** The exact command whose output confirms the
   claim. For a story, that is the project's full verification gate. For a bug
   fix, the reproduction case now passing **plus** the full gate.

2. **Run it fresh, now.** Not a remembered run from earlier in the session. If
   anything changed since the last run — even a one-line refactor — the earlier
   output is stale.

3. **Read the full output and the exit code.** The whole thing, not the first
   line. Count the failures. A suite that prints progress dots can still end in
   a failure summary, and a non-zero exit code can hide below a screen of
   reassuring output.

4. **Check the claim against the evidence.** Does the output actually support
   what you are about to say? A green linter is not a passing test suite. A
   passing unit test is not a working end-to-end flow. Do not treat one signal
   as another.

5. **Only then, state the result** — with the evidence attached: what you ran
   and what it showed. If the output does not support the claim, report the
   actual status instead, with the same evidence.

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

## What proof each claim actually needs

The trap is accepting a weaker signal as if it were the real proof. Each row
below pairs a claim with the evidence that supports it and the things that look
like evidence but are not.

| Claim | Requires | Not sufficient |
|-------|----------|----------------|
| Tests pass | The test command's output now, showing 0 failures | A previous run; "it should pass" |
| Linter clean | The linter's output now, showing 0 errors | A partial check; extrapolating from one file |
| Types check | `mypy` output now, exit 0 | The linter passing; the code "looks typed" |
| Build succeeds | The build command exiting 0 | The linter passing; logs that look fine |
| Bug fixed | The original failing case, retested, now passing | The code changed; assuming it is fixed |
| Regression test works | A red→green cycle: seen it fail, then pass | The test passing once after the fix |
| Subagent completed | A VCS diff showing the actual changes | The agent's "success" report |
| Story requirements met | A line-by-line pass over each requirement | The test suite passing |

## Treating one signal as another is forbidden

These substitutions feel reasonable in the moment and are wrong every time:

- A clean `ruff`/`mypy` run is not proof the tests pass.
- A passing unit test is not proof of a working end-to-end flow.
- A successful build is not proof of behaviour.
- A subagent's or tool's "done" is not proof — re-run the proof yourself. The
  agent reports what it intended; the diff and the gate report what happened.

## Red flags — pause and run the gate

If you notice yourself doing any of these, stop and verify before continuing:

- Reaching for "should", "probably", or "seems to".
- Writing "Great!", "Perfect!", or "Done!" before any command has been run.
- About to commit, push, or open a PR without a fresh gate run.
- Taking a subagent's or tool's success report at face value.
- Leaning on a partial check to stand in for the whole gate.
- Thinking "just this once" or wanting to be finished because it's late.

## When you're tempted to skip it

| Thought | Reality |
|---------|---------|
| "It should work now" | Then the gate will confirm it — run it. |
| "I'm confident" | Confidence is not evidence. |
| "Just this once" | The one you skip is the one that breaks. |
| "The linter passed" | The linter is not the compiler or the tests. |
| "The subagent said it succeeded" | Verify it independently against the diff. |
| "A partial check is enough" | A partial check proves only the part you ran. |
| "I worded it differently, so this doesn't apply" | The rule is about the spirit, not the phrasing. |

## Done means

A story is done when, in a single fresh run, the full gate is green **and** the
behaviour has been observed — the functional test passing, or a real run of the
feature. Only then mark the story `done` and commit.

---

_Adapted from [superpowers](https://github.com/obra/superpowers) by Jesse Vincent (MIT License, © 2025), merged with project standards._
