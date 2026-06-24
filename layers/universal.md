# Universal AI Coding Standards

The single source of truth for how code is written. These are principles to reason from,
not a checklist to pattern-match.

## Naming

Names state intent in full. A reader should infer purpose from the name alone, without
the surrounding code or conversation.

- Bad: `K`, `mt`, `df2`, `tmp`, `do_it()`, `data2`. These hide intent.
- Good: `beam_width`, `model_tokenizer`, `aligned_pairs`, `compute_edit_labels()`,
  `detection_logits`, `keep_ratio`.
- No abbreviations that are not already domain vocabulary. `edit_distance`, not `ed`.

## Docs

Write the code first and get it correct. Then make a **separate pass** to add docstrings
and comments. Writing both at once produces narration that drifts from the code.

- They explain the **why / business logic**, never restate the **what**. Anyone can read
  the code; the reason behind it is what needs recording.
- They are written for a future reader who has **no access to this conversation**. Never
  use a docstring or comment to address the user or narrate a decision — record the logic.
- No banner / divider comments (`# ----- section -----`). Delete them on sight.
- A docstring that just repeats the signature adds nothing — omit it or explain the logic.
- **Multi-line form always:** opening `"""` on its own line, content indented, closing
  `"""` on its own line — even for a single sentence. Never use the inline form
  `"""one-liner"""`.

## Structure

Single responsibility per unit. Group related behaviour and the state it operates on into
a **class**.

- Model variants with an **abstract base class** — e.g. `Serializer(ABC)` →
  `JsonSerializer`, `CsvSerializer`.
- **Composition is the default for reuse**; inheritance is for genuine polymorphic
  contracts, not for sharing code. Avoid deep hierarchies.
- Do **not** wrap a single stateless function in a class for its own sake. A pure
  transform with no state is a function.

## Craft

No on-the-fly, half-finished, or "simplified-to-pass" code. If something is worth
writing, it is written to standard the first time — not patched in later. A quick
experiment lives inline (a one-off command) or under a dedicated `scripts/` directory,
never scattered through the source. Reviews and research are **loops, not one pass**, and
prompts to a reviewer are **neutral** — state the artifact and ask what is wrong, never
state the answer you hope for (a leading prompt produces confirmation, not signal).

## Tests

Plan the tests and have the reviewer challenge them **before** writing them. Then drive
the code test-first.

- **Unit** tests for isolated logic; **functional** tests for an end-to-end scenario.
- **Arrange–Act–Assert**, with a blank line separating the three segments.
- Each test has a **docstring** (multi-line form, per the Docs rule) stating the logic
  under test — the scenario and expected behaviour, not a description of the code.
- Test names state the scenario: `test_already_correct_input_is_left_unchanged`,
  not `test_1`.
- **Value over coverage.** Test behaviour that can break and matters; do not assert the
  framework or trivially-true facts.
- **Match rigor to the surface.** Fully deterministic logic gets strict red-green TDD.
  Nondeterministic or hard-to-pin surfaces are tested for mechanics and invariants —
  shapes, round-trips, seeded reproducibility — not exact outputs.
- A claim of success is backed by fresh command output, never by assumption.

## Git

Follow [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/).

- **Message:** `<type>(<scope>): <subject>`, referencing the story code.
  Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`,
  `chore`, `revert`. Breaking change: `!` after the type/scope.
- **Trailer:** `Co-Authored-By: Claude <model> <noreply@anthropic.com>`.
- **Branch:** `<type>/<story-code>-<short-name>`, one branch per story, merged to `main`
  when the story is done.

## Workflow

Every story follows the same lifecycle. Invoke the corresponding skill at each step.

| Step | When | Skill |
|------|------|-------|
| Plan | Before writing any code | `plan-task` |
| Implement | One story at a time | `test-driven-development` |
| Verify | Before marking a story done | `verification-before-completion` |
| Review | After verification passes | `reviewer-loop` |
| Debug | When a test fails unexpectedly | `systematic-debugging` |

The `review` skill runs a single pass inside `reviewer-loop`. Use `reviewer-loop` to reach convergence.
