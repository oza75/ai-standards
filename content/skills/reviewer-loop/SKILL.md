---
name: reviewer-loop
description: Review is a loop, not one pass — run review with claude-opus-4-8 and iterate until a full pass yields no new CRITICAL or MAJOR findings.
---

# reviewer-loop

**The Law:** Review is a loop, not one pass. Run → review → collect findings →
address → re-review → repeat until a full pass yields **no new CRITICAL or MAJOR
findings**. One clean-looking pass is never "done" — it can be a fluke.

This skill wraps the `review` skill with the loop discipline. Each pass runs as
an **independent reviewer**, always on **claude-opus-4-8**:

- On **Claude Code**, delegate each pass to the `reviewer` subagent (defined in
  `.claude/agents/`) — it is read-only, runs on claude-opus-4-8, and applies the
  `review` skill (to code or to a plan) in an isolated context.
- On **GitHub Copilot**, use the `reviewer` custom agent (`.github/agents/`).
- On **Cursor** (no file-based subagent), run the `review` skill directly.

Running review in a separate agent matters: a fresh context with no stake in the
implementation reviews the change on its own terms.

## The loop

1. Run a review pass — hand the reviewer the change in scope and the acceptance
   criteria (or the story set / plan being reviewed).
2. Separate **new findings this round** from ones already raised.
3. If any CRITICAL or MAJOR findings exist: address every one, then return to
   step 1.
4. When a full pass yields no new CRITICAL or MAJOR findings, the loop has
   **converged** — say so explicitly ("converged — safe to proceed") and stop.

## Neutral prompts

The prompt to the reviewer must be **neutral**. State the artifact and ask "what
is wrong, missing, or unjustified?" — never state your conclusion, hypothesis, or
the answer you are hoping for. A leading prompt produces confirmation, not
signal.

## Rules

- Always use **claude-opus-4-8** (or better). Never use a smaller model to review.
- CRITICAL and MAJOR block and must be addressed. MINOR and NIT are fix-or-note,
  not blocking.
- Track the rounds — note when each pass finds no new blocking findings; that is
  the convergence signal.
- Do not stop on the first pass that looks clean. Loop until a pass is *genuinely*
  clean.
- Feed the reviewer both the acceptance criteria and the implementation — a
  review without the criteria cannot check intent fidelity.
