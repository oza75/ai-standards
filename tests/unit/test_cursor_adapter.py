import tempfile
from pathlib import Path

import yaml

from ai_standards.adapters.cursor import CursorAdapter

_UNIVERSAL = "# Universal\n\nUniversal coding standards.\n"
_PYTHON = "# Python\n\nPython-specific standards.\n"
_SKILL_PLAN_TASK = (
    "---\nname: plan-task\ndescription: Plan a task.\n---\n\n# plan-task\n"
)
_SKILL_REVIEW = "---\nname: review\ndescription: Review code.\n---\n\n# review\n"


def test_creates_agents_md() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        CursorAdapter.run(
            project_dir,
            layers={"universal": _UNIVERSAL},
            skill_plan_task=_SKILL_PLAN_TASK,
            skill_review=_SKILL_REVIEW,
        )

        assert (project_dir / "AGENTS.md").exists()


def test_agents_md_has_universal_content() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        CursorAdapter.run(
            project_dir,
            layers={"universal": _UNIVERSAL},
            skill_plan_task=_SKILL_PLAN_TASK,
            skill_review=_SKILL_REVIEW,
        )

        content = (project_dir / "AGENTS.md").read_text(encoding="utf-8")
        assert _UNIVERSAL in content


def test_creates_python_mdc_when_python_in_languages() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        CursorAdapter.run(
            project_dir,
            layers={"universal": _UNIVERSAL, "python": _PYTHON},
            skill_plan_task=_SKILL_PLAN_TASK,
            skill_review=_SKILL_REVIEW,
        )

        assert (project_dir / ".cursor" / "rules" / "python.mdc").exists()


def test_no_python_mdc_when_python_absent() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        CursorAdapter.run(
            project_dir,
            layers={"universal": _UNIVERSAL},
            skill_plan_task=_SKILL_PLAN_TASK,
            skill_review=_SKILL_REVIEW,
        )

        assert not (project_dir / ".cursor" / "rules" / "python.mdc").exists()


def test_python_mdc_frontmatter_always_apply() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        CursorAdapter.run(
            project_dir,
            layers={"universal": _UNIVERSAL, "python": _PYTHON},
            skill_plan_task=_SKILL_PLAN_TASK,
            skill_review=_SKILL_REVIEW,
        )

        text = (project_dir / ".cursor" / "rules" / "python.mdc").read_text(
            encoding="utf-8"
        )
        _, fm_text, _ = text.split("---", 2)
        fm = yaml.safe_load(fm_text)
        assert fm.get("alwaysApply") is True
        assert "globs" not in fm


def test_python_mdc_has_python_body() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        CursorAdapter.run(
            project_dir,
            layers={"universal": _UNIVERSAL, "python": _PYTHON},
            skill_plan_task=_SKILL_PLAN_TASK,
            skill_review=_SKILL_REVIEW,
        )

        text = (project_dir / ".cursor" / "rules" / "python.mdc").read_text(
            encoding="utf-8"
        )
        _, _, body = text.split("---", 2)
        assert _PYTHON.strip() in body


def test_creates_plan_task_skill() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        CursorAdapter.run(
            project_dir,
            layers={"universal": _UNIVERSAL},
            skill_plan_task=_SKILL_PLAN_TASK,
            skill_review=_SKILL_REVIEW,
        )

        assert (project_dir / ".cursor" / "skills" / "plan-task" / "SKILL.md").exists()


def test_creates_review_skill() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        CursorAdapter.run(
            project_dir,
            layers={"universal": _UNIVERSAL},
            skill_plan_task=_SKILL_PLAN_TASK,
            skill_review=_SKILL_REVIEW,
        )

        assert (project_dir / ".cursor" / "skills" / "review" / "SKILL.md").exists()


def test_skill_name_matches_folder() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        CursorAdapter.run(
            project_dir,
            layers={"universal": _UNIVERSAL},
            skill_plan_task=_SKILL_PLAN_TASK,
            skill_review=_SKILL_REVIEW,
        )

        for folder, content in [
            ("plan-task", _SKILL_PLAN_TASK),
            ("review", _SKILL_REVIEW),
        ]:
            text = (project_dir / ".cursor" / "skills" / folder / "SKILL.md").read_text(
                encoding="utf-8"
            )
            _, fm_text, _ = text.split("---", 2)
            fm = yaml.safe_load(fm_text)
            assert fm["name"] == folder


def test_gitignore_not_touched() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        CursorAdapter.run(
            project_dir,
            layers={"universal": _UNIVERSAL},
            skill_plan_task=_SKILL_PLAN_TASK,
            skill_review=_SKILL_REVIEW,
        )

        assert not (project_dir / ".gitignore").exists()


def test_rerun_overwrites_cleanly() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)
        layers = {"universal": _UNIVERSAL, "python": _PYTHON}

        CursorAdapter.run(
            project_dir,
            layers=layers,
            skill_plan_task=_SKILL_PLAN_TASK,
            skill_review=_SKILL_REVIEW,
        )
        paths = [
            project_dir / "AGENTS.md",
            project_dir / ".cursor" / "rules" / "python.mdc",
            project_dir / ".cursor" / "skills" / "plan-task" / "SKILL.md",
            project_dir / ".cursor" / "skills" / "review" / "SKILL.md",
        ]
        first = {str(p): p.read_bytes() for p in paths}

        CursorAdapter.run(
            project_dir,
            layers=layers,
            skill_plan_task=_SKILL_PLAN_TASK,
            skill_review=_SKILL_REVIEW,
        )

        for p in paths:
            assert p.read_bytes() == first[str(p)]


def test_returns_written_paths_python() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        result_with_python = CursorAdapter.run(
            project_dir,
            layers={"universal": _UNIVERSAL, "python": _PYTHON},
            skill_plan_task=_SKILL_PLAN_TASK,
            skill_review=_SKILL_REVIEW,
        )
        assert len(result_with_python) == 4
        assert "AGENTS.md" in result_with_python
        assert ".cursor/rules/python.mdc" in result_with_python
        assert ".cursor/skills/plan-task/SKILL.md" in result_with_python
        assert ".cursor/skills/review/SKILL.md" in result_with_python

    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        result_no_python = CursorAdapter.run(
            project_dir,
            layers={"universal": _UNIVERSAL},
            skill_plan_task=_SKILL_PLAN_TASK,
            skill_review=_SKILL_REVIEW,
        )
        assert len(result_no_python) == 3
        assert ".cursor/rules/python.mdc" not in result_no_python
