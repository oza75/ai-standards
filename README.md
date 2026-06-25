# ai-standards

A portable Python CLI that manages your personal AI coding standards across
**Claude Code**, **Cursor**, and **VS Code Copilot**.

You keep one canonical set of standards in `~/.ai-standards/`. Per project, the
tool deploys them in each tool's **native format** — instructions, skills, a
reviewer subagent, and a Context7 docs server — so every AI assistant you use
follows the same workflow and conventions. All deployed files are **gitignored**:
these are your personal standards, not team config.

## What gets deployed

Running `ai-standards init` in a project writes (and gitignores):

| Tool | Files |
|------|-------|
| **Shared** | `AGENTS.md` (universal standards — read natively by Cursor & Copilot, imported by Claude Code) |
| **Claude Code** | `CLAUDE.local.md` (`@AGENTS.md` + language layers), `.claude/skills/<name>/`, `.claude/agents/reviewer.md`, `.mcp.json` |
| **Cursor** | `.cursor/skills/<name>/`, `.cursor/rules/python.mdc`, `.cursor/mcp.json` |
| **Copilot** | `.github/copilot-instructions.md`, `.github/skills/<name>/`, `.github/agents/reviewer.agent.md`, `.vscode/mcp.json` |

The **skills** encode a test-first workflow as a loop across two phases:

- **Plan** — `plan-task` decomposes a goal into reviewer-converged user stories.
- **Code** — `implement-story` builds each story: `test-driven-development` →
  `verification-before-completion` → `reviewer-loop` (delegating to the
  `reviewer` subagent) → commit.
- Cross-cutting: `systematic-debugging` (root cause before any fix) and
  `read-docs` (pull current, version-correct library docs via Context7 before
  writing against a dependency).

## Install

Requires [`uv`](https://docs.astral.sh/uv/) and Python ≥ 3.11.

```bash
uv tool install git+https://github.com/oza75/ai-standards
```

This puts the `ai-standards` command on your PATH. To upgrade later:

```bash
uv tool upgrade ai-standards
```

## Usage

### 1. Install the canonical standards (once per machine)

```bash
ai-standards install
```

Downloads the layer files and skill/agent content into `~/.ai-standards/`.
Re-run any time to refresh it (atomic — a failed download never corrupts the
existing store).

### 2. Deploy into a project

From the root of a project:

```bash
ai-standards init
```

Detects the project's language(s), assembles the right layers, and writes the
per-tool files above — adding each to the project's `.gitignore` under a managed
block. Language detection can be forced:

```bash
ai-standards init --python        # force the Python layer
ai-standards init --typescript    # detected, but no adapter yet — deploys universal only
```

### 3. Re-sync after editing your standards

If you change files in `~/.ai-standards/`, re-deploy them into the current
project:

```bash
ai-standards sync
```

### 4. Update everything

Pull the latest canonical standards from this repo **and** re-deploy them into
the current project in one step:

```bash
ai-standards update
```

## Context7 (live documentation)

`init` deploys a [Context7](https://github.com/upstash/context7) MCP server
config for each tool (local `npx -y @upstash/context7-mcp`, **no API key** — so
nothing secret is written). Context7 serves up-to-date, version-specific library
docs, which the `read-docs` skill uses to avoid coding against stale/hallucinated
APIs.

On first use in a project, each tool will **prompt you to approve** the
`context7` MCP server — this is the tools' standard trust gate for any
project-scoped MCP server. Approve it once per project.

An API key is optional and only raises rate limits; if you want one, set
`CONTEXT7_API_KEY` in your environment (never commit it).

## Customizing your standards

The canonical content lives in this repo and, after `install`, in
`~/.ai-standards/`:

- `layers/universal.md` — language-agnostic standards (the spine).
- `layers/python.md`, `layers/typescript.md` — language layers.
- `content/skills/<name>/SKILL.md` — the workflow skills.
- `content/claude/agents/reviewer.md`, `content/copilot/agents/reviewer.agent.md`
  — the reviewer personas.

Edit them to taste, then `ai-standards sync` (or `update`) to push the changes
into your projects. The file list deployed by the tool is driven by
`layers/manifest.json`.

## Development

The project runs locally with `uv`:

```bash
make check    # ruff check + ruff format --check + mypy + pytest
make test     # pytest only
make lint     # ruff check + ruff format --check
```

## Scope & limitations

- Deployed files are gitignored by design — personal standards, not team config.
- The TypeScript **adapter** is not implemented yet (the detector recognizes TS,
  but `init` deploys the universal layer only when TS is detected).
- `clean`/`uninstall` and `status`/`list` commands are not implemented yet.
- Cursor's reviewer "agent" is a UI-only Custom Mode, so on Cursor the review
  runs as the `review` skill rather than a deployed subagent file.
