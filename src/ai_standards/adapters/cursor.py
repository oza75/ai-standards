from pathlib import Path


class CursorAdapter:
    @staticmethod
    def run(
        project_dir: Path,
        layers: dict[str, str],
        skills: dict[str, str],
    ) -> list[str]:
        written: list[str] = []

        for name, content in skills.items():
            skill_dir = project_dir / ".cursor" / "skills" / name
            skill_dir.mkdir(parents=True, exist_ok=True)
            (skill_dir / "SKILL.md").write_text(content, encoding="utf-8")
            written.append(f".cursor/skills/{name}/SKILL.md")

        if "python" in layers:
            rules_dir = project_dir / ".cursor" / "rules"
            rules_dir.mkdir(parents=True, exist_ok=True)
            mdc = "---\nalwaysApply: true\n---\n\n" + layers["python"]
            (rules_dir / "python.mdc").write_text(mdc, encoding="utf-8")
            written.append(".cursor/rules/python.mdc")

        return written
