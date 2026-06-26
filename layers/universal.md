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

## Design

Code is designed, not accreted. Model the domain in **objects**: group related behaviour
with the state it acts on into a class that has a single, clear responsibility. Default to
OOP wherever there is state to hold, variation to absorb, or a contract to uphold —
prefer an explicit object over loose functions threading dictionaries between them.

- **Reach for the design pattern that fits the problem, and name it** so the intent is
  legible: Strategy for interchangeable algorithms, Factory for construction that varies,
  Adapter to bridge an external interface to yours, Template Method / ABC for a fixed
  skeleton with varying steps, Observer for event fan-out, Repository to isolate storage.
  Do not force a pattern where a plain function or class is clearer — a pattern applied
  for its own sake is just indirection with a fancy name.
- **Model variants with an abstract base class** — e.g. `Serializer(ABC)` →
  `JsonSerializer`, `CsvSerializer`. Program to the interface, not the concrete type, so a
  new variant slots in without editing the call sites.
- **Single responsibility, open to extension.** A unit does one thing; adding a case
  should mean adding a class, not growing an `if/elif` chain. Depend on abstractions, not
  concretions, so pieces swap out and test in isolation.
- **Composition is the default for reuse**; inheritance is for genuine polymorphic
  contracts, not for sharing code. Avoid deep hierarchies.
- Do **not** wrap a single stateless function in a class for its own sake. A pure
  transform with no state is a function. "OOP whenever possible" means whenever there is
  something to model — not ceremony around nothing.

## Performance

Efficiency is a design property, chosen up front — not a patch applied later. Write code
that is fast and frugal **by construction**, then measure to confirm. The largest wins
come from the **right algorithm and data structure**, so get the complexity right before
tuning constants: an O(n²) pass over a real dataset is the bug, not the missing
micro-optimisation.

- **Memory.** Stream rather than materialise — iterate, generate, and process in chunks
  instead of loading a whole dataset into memory at once. Avoid needless copies and
  throwaway intermediate collections; release what you no longer need.
- **Parallelism — when the work is genuinely parallel and large enough to pay for it.**
  I/O-bound fan-out (network, disk, API calls) overlaps with async or a thread pool;
  CPU-bound work parallelises with a process pool or vectorisation, not threads contending
  on a lock. Match the mechanism to the bottleneck instead of reaching for the same tool
  every time. Size and reuse pools deliberately — do not spawn workers without bound.
- **Measure before micro-tuning.** Profile to find the real hot path; do not guess. But
  "measure first" is not licence to write knowingly wasteful code — the obvious efficient
  form is the one to write first.
- Efficiency never excuses unreadable code. When fast and clear genuinely conflict, keep
  the surface clear and isolate the hot, optimised part behind a clean interface with a
  comment recording why.

## Craft

No on-the-fly, half-finished, or "simplified-to-pass" code. If something is worth
writing, it is written to standard the first time — not patched in later. A quick
experiment lives inline (a one-off command) or under a dedicated `scripts/` directory,
never scattered through the source. Reviews and research are **loops, not one pass**, and
prompts to a reviewer are **neutral** — state the artifact and ask what is wrong, never
state the answer you hope for (a leading prompt produces confirmation, not signal).

## Research

The single most important habit. Hallucinated APIs and outdated signatures are the
leading cause of broken code, and training memory is the source — it blends versions and
is confidently wrong about the exact call you are about to depend on. So whenever you
**use, choose, design against, or debug** an external library, framework, or API,
retrieve its current, version-correct documentation with the `read-docs` skill (backed by
Context7) **before** you decide or write — never from memory.

This is **continuous, not a one-time step**. It applies at every point a decision touches
a dependency:

- **Planning** — research the libraries a task touches before proposing an approach; a
  plan built on a remembered API collapses on contact with the real one.
- **Coding** — pull the current docs before writing each call against a dependency.
- **Reviewing** — flag any external API used without verification; an unverified call is
  a finding.
- **Debugging** — when a library behaves unexpectedly, suspect a version/API mismatch and
  re-read its docs before theorising about your own code.

Retrieve **correctly**: the right library (not a fork or same-named package), the version
the project actually pins, and a query for the specific thing you need. The retrieved docs
are ground truth — when they conflict with memory, the docs win. If you cannot retrieve
them, say so; never present a guess as fact.

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

The workflow is a **loop**, run in **two phases**. Each phase has an entry skill the
tool invokes automatically — you do not run the steps by hand. Neither phase is a
straight line: each repeats until it converges.

**Planning phase — loop until the story set converges.** Driven by `plan-task`:
propose the story set → `reviewer-loop` challenges the decomposition → revise →
re-review, repeating until no CRITICAL/MAJOR remains. Only then write the story files,
and run `reviewer-loop` once more on what was written. No code is written until this
converges.

**Coding phase — loop per story until done.** Driven by `implement-story`, which takes
one story at a time in dependency order through: `test-driven-development` (red → green →
refactor, one unit at a time, itself a loop) → `verification-before-completion` (the full
gate green, with the behaviour observed) → `reviewer-loop` (repeat until no
CRITICAL/MAJOR) → commit → next story.

`systematic-debugging` is invoked whenever a test fails for a non-obvious reason — root
cause before any fix.

| Phase | Entry skill | Loops until |
|-------|-------------|-------------|
| Plan | `plan-task` | story set has no CRITICAL/MAJOR |
| Code (per story) | `implement-story` (nests `test-driven-development` → `verification-before-completion` → `reviewer-loop`) | gate green and review converged |
| Debug (as needed) | `systematic-debugging` | root cause found, regression test passes |

`plan-task` plans only and hands off to `implement-story` to build. `review` runs a
single pass; `reviewer-loop` runs it to convergence. `read-docs` is **cross-cutting** —
not a phase but a discipline invoked throughout: before planning an approach, before
writing each call against a dependency, while reviewing for unverified APIs, and while
debugging a library that behaves unexpectedly. Consult current docs (Context7) rather than
memory at every point a decision touches an external dependency.
