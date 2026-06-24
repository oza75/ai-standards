from pathlib import Path


class CursorAdapter:
    @staticmethod
    def run(
        project_dir: Path,
        layers: dict[str, str],
        skill_plan_task: str,
        skill_review: str,
    ) -> list[str]:
        written: list[str] = []

        (project_dir / "AGENTS.md").write_text(layers["universal"], encoding="utf-8")
        written.append("AGENTS.md")

        if "python" in layers:
            rules_dir = project_dir / ".cursor" / "rules"
            rules_dir.mkdir(parents=True, exist_ok=True)
            mdc = "---\nalwaysApply: true\n---\n\n" + layers["python"]
            (rules_dir / "python.mdc").write_text(mdc, encoding="utf-8")
            written.append(".cursor/rules/python.mdc")

        for folder, content in [
            ("plan-task", skill_plan_task),
            ("review", skill_review),
        ]:
            skill_dir = project_dir / ".cursor" / "skills" / folder
            skill_dir.mkdir(parents=True, exist_ok=True)
            (skill_dir / "SKILL.md").write_text(content, encoding="utf-8")
            written.append(f".cursor/skills/{folder}/SKILL.md")

        return written
