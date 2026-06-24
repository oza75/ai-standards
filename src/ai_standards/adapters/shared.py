from pathlib import Path


class SharedAdapter:
    """Writes the cross-tool standards file every AI tool reads.

    `AGENTS.md` is the shared entry point: Cursor and GitHub Copilot read it
    natively, and Claude Code imports it via `@AGENTS.md` from CLAUDE.local.md.
    It is owned here — not by any single tool's adapter — so its creation is
    explicit rather than a side effect of one tool's deployment.
    """

    @staticmethod
    def run(project_dir: Path, layers: dict[str, str]) -> list[str]:
        (project_dir / "AGENTS.md").write_text(
            layers.get("universal", ""), encoding="utf-8"
        )
        return ["AGENTS.md"]
