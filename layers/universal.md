# Universal AI Coding Standards

Personal coding standards applied across all projects and languages.

## Naming

- Names reveal intent; avoid abbreviations unless universally known (`url`, `id`, `ctx`).
- Boolean names start with `is_`, `has_`, or `can_` (`is_valid`, `has_children`).
- Functions and methods are verbs or verb phrases (`get_user`, `validate_input`).
- Avoid generic names: `data`, `info`, `result`, `temp`, `x` — name what it represents.

## Docs

- Write no comments by default. Add one only when the WHY is non-obvious: a hidden
  constraint, a subtle invariant, or a workaround for a specific bug.
- Never describe WHAT the code does (well-named identifiers already do that).
- Public API functions get a one-line summary only if the name alone is insufficient.
- No multi-line docblocks for internal helpers.

## Tests

- Tests are the first code written (TDD). Write a failing test before any production code.
- Each test asserts one behaviour. Name tests `test_<what>_<condition>_<expected>`.
- No mocking of things you own — prefer real objects or fakes over mocks.
- Test the contract (inputs/outputs), not the implementation details.
- Every edge case that caused a bug gets a regression test.

## Git

- Conventional Commits: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`.
- One logical change per commit. Commits are not checkpoints — they are history.
- Commit message subject ≤ 72 chars; imperative mood ("Add …", not "Added …").
- Never amend or force-push commits that have been shared.
