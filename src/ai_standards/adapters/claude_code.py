from pathlib import Path


class ClaudeCodeAdapter:
    """Deploys Claude Code's native files.

    Claude Code reads `CLAUDE.local.md` (gitignored personal layer) and skills
    under `.claude/commands/`. It does not read `AGENTS.md` natively, so the
    universal layer is pulled in via the `@AGENTS.md` import directive on the
    first line of CLAUDE.local.md. `AGENTS.md` itself is written by SharedAdapter.
    """

    @staticmethod
    def run(
        project_dir: Path,
        layers: dict[str, str],
        skills: dict[str, str],
    ) -> list[str]:
        lang_layers = [layers[k] for k in sorted(k for k in layers if k != "universal")]
        parts: list[str] = ["@AGENTS.md"] + [p.rstrip() for p in lang_layers]
        (project_dir / "CLAUDE.local.md").write_text(
            "\n\n".join(parts) + "\n", encoding="utf-8"
        )

        commands_dir = project_dir / ".claude" / "commands"
        commands_dir.mkdir(parents=True, exist_ok=True)
        for name, content in skills.items():
            (commands_dir / f"{name}.md").write_text(content, encoding="utf-8")

        return ["CLAUDE.local.md", ".claude/commands/"]
