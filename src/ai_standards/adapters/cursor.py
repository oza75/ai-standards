from pathlib import Path

from ai_standards.mcp import context7_server, merge_mcp_server


class CursorAdapter:
    @staticmethod
    def run(
        project_dir: Path,
        layers: dict[str, str],
        skills: dict[str, dict[str, str]],
    ) -> list[str]:
        written: list[str] = []

        for name, files in skills.items():
            skill_dir = project_dir / ".cursor" / "skills" / name
            for inner, content in files.items():
                dest = skill_dir / inner
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_text(content, encoding="utf-8")
                written.append(f".cursor/skills/{name}/{inner}")

        if "python" in layers:
            rules_dir = project_dir / ".cursor" / "rules"
            rules_dir.mkdir(parents=True, exist_ok=True)
            mdc = "---\nalwaysApply: true\n---\n\n" + layers["python"]
            (rules_dir / "python.mdc").write_text(mdc, encoding="utf-8")
            written.append(".cursor/rules/python.mdc")

        merge_mcp_server(
            project_dir / ".cursor" / "mcp.json",
            "mcpServers",
            "context7",
            context7_server(include_type=False),
        )
        written.append(".cursor/mcp.json")

        return written
