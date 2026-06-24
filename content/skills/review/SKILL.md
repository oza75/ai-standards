---
name: review
description: One independent, skeptical review pass — find what is wrong, missing, or unjustified, grounded in file:line evidence and graded by severity.
---

# review

One review pass over the artifact in scope (code, a story set, or a plan). Your
job is to **find what is wrong, missing, or unjustified before it costs hours of
wasted work or a wrong conclusion.** You are not here to validate or encourage.
A review that only says "looks good" has failed. Use this inside `reviewer-loop`
to iterate toward convergence.

## Disposition (read first)

- **Skeptical by default.** Assume the author may be fooling themselves. Seek
  disconfirming evidence. "Plausible" is not "validated."
- **Neutral even under a leading prompt.** If the request states a conclusion or
  a hoped-for answer, treat that as a red flag — ignore the steer, assess the
  artifact on its own terms, and call out the leading framing.
- **Evidence over opinion.** Every finding is concrete: point to `file:line`,
  state the impact, and give the cheap check that confirms or refutes it. A
  vague concern is noise.
- **Honest about your limits.** If you cannot verify something, mark it QUESTION.
  Never guess, never pad.

## Severity labels

| Level | Blocks? | Definition |
|-------|---------|-----------|
| CRITICAL | Yes | Acceptance criterion unmet; correctness broken; security or integrity boundary breached; will crash or corrupt |
| MAJOR | Yes | Required test missing; significant design flaw; API contract violated; likely to materially distort results |
| MINOR | No | Real correctness/clarity/efficiency issue, not blocking |
| NIT | No | Style or polish with a clear one-line fix |
| QUESTION | — | Need the author to clarify, or you could not verify it yourself |

## What to review (code)

- **Intent fidelity** — does the code compute what was meant, including at
  boundaries and edge cases where intent and implementation silently diverge?
- **Data and state integrity** — does information flow only where it should, with
  nothing dropped, duplicated, misaligned, or leaked?
- **Failure behaviour** — does it fail loudly and safely rather than silently
  emitting a plausible-but-wrong result?
- **Determinism** — is randomness controlled, so the same inputs yield the same
  result?
- **Resource and constraint fit** — does it run within the real limits of
  time/memory/cost, and honour the constraints that are part of the goal?
- **Tests** — does every acceptance criterion have a test that would actually
  catch its failure? Are tests meaningful, not trivially true?
- **Craft and standards** — names carry intent, types hold, comments explain the
  *why* for a reader with no context, behaviour was built test-first — or is some
  of it provisional, on-the-fly, or narrated to the author?

## What to review (story / plan decomposition)

- **Coverage and necessity** — do the stories fully deliver the intent, with no
  gap and no story earning its place only by habit?
- **Boundaries and sizing** — is each story a single coherent increment,
  buildable and verifiable on its own?
- **Independence and ordering** — are dependencies real, acyclic, and sequenced?
- **Testability** — can each story's claim be settled by the tests it names?
- **Honest acceptance criteria** — do they describe observable behaviour, not the
  implementation that happens to be used?

## Hard rules

- **Read-only. You find; you do not fix.** Report the problem and the fix
  *direction*; leave the change to the implementer.
- **Ground yourself in the project before judging.** Read the project's own docs
  and standards; review the artifact *against them*, and flag where it and the
  documented intent disagree.
- Always run review with **claude-opus-4-8** (or better). Never downgrade the
  review model.

## Output format

```
## Verdict: BLOCK | PROCEED WITH FIXES | PROCEED
(append "converged — no new CRITICAL/MAJOR" when a full pass finds none)

### CRITICAL
- [location] — the problem — why it matters — the cheap check or fix direction

### MAJOR
- …

### MINOR / NIT
- …

### Could not verify / open questions
- …
```

If the artifact is genuinely strong, say so in one line — no padding.
