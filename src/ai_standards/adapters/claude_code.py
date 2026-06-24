from pathlib import Path


class ClaudeCodeAdapter:
    """Deploys Claude Code's native files.

    Claude Code reads `CLAUDE.local.md` (gitignored personal layer) and Skills
    under `.claude/skills/<name>/SKILL.md`. Skills are *model-invoked* — Claude
    triggers them automatically from their `description`, which is what makes the
    deployed workflow self-driving (unlike `.claude/commands/`, which only run
    when the user types `/name`). It does not read `AGENTS.md` natively, so the
    universal layer is pulled in via the `@AGENTS.md` import directive on the
    first line of CLAUDE.local.md. `AGENTS.md` itself is written by SharedAdapter.
    """

    @staticmethod
    def run(
        project_dir: Path,
        layers: dict[str, str],
        skills: dict[str, dict[str, str]],
    ) -> list[str]:
        lang_layers = [layers[k] for k in sorted(k for k in layers if k != "universal")]
        parts: list[str] = ["@AGENTS.md"] + [p.rstrip() for p in lang_layers]
        (project_dir / "CLAUDE.local.md").write_text(
            "\n\n".join(parts) + "\n", encoding="utf-8"
        )

        written = ["CLAUDE.local.md"]
        for name, files in skills.items():
            skill_dir = project_dir / ".claude" / "skills" / name
            for inner, content in files.items():
                dest = skill_dir / inner
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_text(content, encoding="utf-8")
                written.append(f".claude/skills/{name}/{inner}")

        return written
