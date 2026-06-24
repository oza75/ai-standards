# STD · ai-standards CLI

## Context

Personal AI coding-standards management tool. Keeps a canonical set of
layer files (`~/.ai-standards/`) downloaded from this GitHub repo and
deploys them per-project — gitignored — into each AI tool's native format.
Supports Claude Code, Cursor, and VS Code Copilot.

Motivation: one source of truth for personal coding standards that works
across every project and every AI coding tool without polluting project git
history.

## Constraints

- Python package, `src/` layout, `mypy --strict`, `ruff`, `pytest`
- CLI via `typer` or `click`; HTTP via `httpx`
- Installed with `uv tool install git+https://github.com/oza/ai-standards`
- All deployed files are gitignored (personal standards, not team config)
- TypeScript adapter explicitly out of scope for this task (detector
  supports it, adapters do not; `init` warns and deploys universal only)
- `clean`/`uninstall` and `status`/`list` commands deferred to follow-on task

## References

- [Cursor rules docs](https://cursor.com/docs/context/rules)
- [Cursor skills docs](https://cursor.com/docs/skills) — verify `.cursor/skills/<name>/SKILL.md` before coding STD-9
- [Claude Code memory docs](https://code.claude.com/docs/en/memory) — `CLAUDE.local.md` is the documented gitignored personal slot
- [VS Code custom agents](https://code.visualstudio.com/docs/agent-customization/custom-agents)
- [VS Code prompt files](https://code.visualstudio.com/docs/copilot/customization/prompt-files)
- [GitHub Copilot custom instructions](https://docs.github.com/en/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot)

## User Stories

- [STD-1 — Package scaffold](user-stories/STD-1-package-scaffold.md)
- [STD-2 — Layer file content](user-stories/STD-2-layer-file-content.md)
- [STD-2b — Tool adapter content files](user-stories/STD-2b-adapter-content-files.md)
- [STD-3 — Language detector](user-stories/STD-3-language-detector.md)
- [STD-4 — Canonical source descriptor](user-stories/STD-4-canonical-source-descriptor.md)
- [STD-5 — Canonical store](user-stories/STD-5-canonical-store.md)
- [STD-6 — install command](user-stories/STD-6-install-command.md)
- [STD-7 — Gitignore manager](user-stories/STD-7-gitignore-manager.md)
- [STD-8 — Claude Code adapter](user-stories/STD-8-claude-code-adapter.md)
- [STD-9 — Cursor adapter](user-stories/STD-9-cursor-adapter.md)
- [STD-10 — VS Code Copilot adapter](user-stories/STD-10-copilot-adapter.md)
- [STD-11 — init command](user-stories/STD-11-init-command.md)
- [STD-12 — sync command](user-stories/STD-12-sync-command.md)
- [STD-13 — update command](user-stories/STD-13-update-command.md)

## Dependency Order

```
STD-1 ∥ STD-2 ∥ STD-2b
  → STD-3 ∥ STD-4 ∥ STD-7      (all need STD-1)
  → STD-5                        (needs STD-4)
  → STD-6                        (needs STD-4, STD-5)
  → STD-8 ∥ STD-9 ∥ STD-10     (all need STD-5; STD-9/10 also need STD-2b)
  → STD-11                       (needs STD-3, STD-6, STD-7, STD-8, STD-9, STD-10)
  → STD-12                       (needs STD-8, STD-9, STD-10, STD-5)
  → STD-13                       (needs STD-6, STD-12)
```
