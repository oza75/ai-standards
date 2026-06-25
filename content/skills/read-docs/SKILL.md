---
name: read-docs
description: Use before writing, choosing, designing against, or debugging any external library, API, framework, SDK, or CLI whose exact current behaviour you are not 100% sure of — signatures, parameters, options, return shapes, config formats, new or deprecated APIs, version differences. Retrieve current, version-correct docs via Context7 first instead of trusting training memory, which is often stale or version-wrong. Triggers during planning (research the libraries a task touches before proposing an approach) and during coding (pull docs before writing against a dependency).
---

# read-docs

**The default:** when you are about to commit to how an external dependency
behaves, read its current docs before you write or decide — do not answer from
memory. Training memory is a snapshot: it blends versions, remembers APIs that
were since renamed or removed, and is confidently wrong about the exact
signature, option name, or return shape you are about to depend on. The cost of
a wrong guess is a plan built on an API that does not exist, or code that fails
in a way that looks like your bug but is really a stale memory.

The point of this skill is not merely "use docs." It is to retrieve the docs
**correctly** — the right library, at the project's version, queried with the
real question, and verified before you trust them. Retrieving the wrong
library's docs, or the wrong major version's, is worse than reading nothing: it
gives you false confidence.

## When this triggers

Any time you are about to **use, choose, design against, or debug** an external
library / API / framework / SDK / CLI and you are not fully certain of its
current behaviour. Concretely:

- You are about to call an API and are unsure of the signature, parameters,
  option names, defaults, or return shape.
- You are choosing between libraries, or designing an approach that leans on
  one — the plan depends on what the library can actually do *now*.
- You hit a config format, migration step, or CLI flag you cannot recall exactly.
- A behaviour surprised you and you suspect an API changed, was deprecated, or
  differs across versions.

When in doubt, read. The few seconds of retrieval are cheaper than building on a
guess.

## Where this fits in the lifecycle

- **Planning** (`plan-task`): before proposing an approach, retrieve current docs
  for the libraries the task touches. A plan that assumes a remembered API can
  collapse the moment you start coding; ground the proposal in what the library
  does today.
- **Coding** (`implement-story`): before writing against a dependency, pull its
  current docs so the code targets the real API, not a recalled one.

## The retrieval pattern

Docs come from **Context7**, an MCP server deployed by this project as `context7`
(local `npx @upstash/context7-mcp`, no API key). It injects up-to-date,
version-specific library documentation.

Context7 works in **two steps**: first resolve a library name to a precise
library ID, then query that library's docs. The tool *names* drift over time —
the docs-query tool was recently renamed from `get-library-docs` to
`query-docs`, for example — so depend on the **pattern**, not exact names. Use
whichever Context7 tools are present:

- a **resolve** tool (e.g. `resolve-library-id`) — takes the library name and
  the task/question; returns Context7 library IDs like `/vercel/next.js` or
  `/mongodb/docs`.
- a **query** tool (e.g. `query-docs`, formerly `get-library-docs`) — takes an
  exact library ID and a specific question; returns docs.

If you do not see these, list the available `context7` tools and use the two
that resolve a library and fetch its docs.

### 1. Resolve the *right* library

Call the resolve tool with **both** the library name and the actual task as the
query — the task text is what ranks the candidates, so a bare name gives you a
worse match. Then disambiguate deliberately. The hazards:

- **Same-named packages** — multiple projects share a name; pick by what you are
  actually doing.
- **Forks and mirrors** — prefer the official/canonical source over a fork.
- **Wrong org** — confirm the org/owner matches the real upstream.

If there is any ambiguity, state which library ID you chose and why. Choosing
the wrong ID here poisons everything downstream — a query against the wrong
library returns plausible, well-formatted, useless docs.

### 2. Match the project's installed version

Before querying, find the version actually in use. Check the dependency
manifest and lockfile — `pyproject.toml` / `uv.lock`, `package.json` /
`package-lock.json`, `go.mod`, etc. Prefer docs for **that** version. Do not
read docs for a different major version than the project pins: a v3 answer
applied to a v2 install is a bug waiting to happen, and the failure will look
like your mistake, not a version mismatch.

### 3. Query with the real question

Pass the **specific** API, feature, or task to the query tool — not just the
library name. Relevance depends on a precise query. Ask for the exact thing you
need: "streaming response API", "migration config options", "how to register a
custom serializer", not "tell me about library X". A vague query returns a vague
overview that rarely contains the detail you came for.

### 4. Verify before you trust

Confirm the returned docs actually correspond to the intended library and
version **and** answer your question. If they are off-target — wrong package,
wrong version, or only tangentially related — re-resolve or refine the query.
Do not settle for "close enough"; tangential docs are how a wrong API sneaks
into your code wearing the costume of a real one.

### 5. Use docs as ground truth

Write or plan against the retrieved API. **If the docs and your memory conflict,
the docs win** — that conflict usually means your memory is from a different
version. Note the version you relied on so a later reader knows what the code
was written against.

### 6. Re-query, do not guess

If the first results do not answer the question, refine and query again — narrow
the topic, rephrase, or split a broad question into specific ones. Never fill a
gap with an assumed API. An invented method name that "sounds right" is the
exact failure this skill exists to prevent.

## When Context7 fails

If Context7 is unavailable, returns nothing useful, or you cannot resolve a
trustworthy library ID, **say so explicitly** — do not quietly fall back to
memory and present a guess as fact. Then fall back to the official first-party
docs (the canonical source for that library, resolved cautiously — the same
disambiguation rules apply). Falling back silently to possibly-stale memory is
the one outcome to avoid: it reintroduces exactly the risk this skill removes,
while hiding that it happened.

## Red flags — stop and retrieve

- You are about to write a method call, option, or config key from memory for an
  external dependency.
- You are proposing an approach that hinges on what a library "can do," unchecked.
- You retrieved docs but never confirmed they match the project's version.
- The query returned tangential results and you are about to use them anyway.
- The docs contradict your memory and you are tempted to trust your memory.
- Context7 failed and you are about to proceed on a guess without saying so.

## Checklist

Before relying on an external dependency's behaviour:

- [ ] Resolved the library with the name **and** the task as the query.
- [ ] Confirmed the library ID is the canonical source (not a fork / wrong org).
- [ ] Checked the manifest/lockfile and targeted the project's installed version.
- [ ] Queried the specific API/feature, not just the library name.
- [ ] Verified the returned docs match the intended library and version.
- [ ] Wrote/planned against the docs, noting the version relied on.
- [ ] If Context7 failed, said so and fell back to first-party docs — not memory.
