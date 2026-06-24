from pathlib import Path


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

        return written
