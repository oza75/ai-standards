import json
import tempfile
from pathlib import Path

import yaml

from ai_standards.adapters.cursor import CursorAdapter

_UNIVERSAL = "# Universal\n\nUniversal coding standards.\n"
_PYTHON = "# Python\n\nPython-specific standards.\n"
_SKILLS = {
    "plan-task": {
        "SKILL.md": (
            "---\nname: plan-task\ndescription: Plan a task.\n---\n\n# plan-task\n"
        ),
    },
    "review": {
        "SKILL.md": "---\nname: review\ndescription: Review code.\n---\n\n# review\n",
    },
    "test-driven-development": {
        "SKILL.md": (
            "---\nname: test-driven-development\ndescription: TDD.\n---\n\n# TDD\n"
        ),
        "testing-anti-patterns.md": "# Testing anti-patterns\n\nDo not test mocks.\n",
    },
}


def test_does_not_write_agents_md() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        CursorAdapter.run(project_dir, layers={"universal": _UNIVERSAL}, skills=_SKILLS)

        assert not (project_dir / "AGENTS.md").exists()


def test_creates_python_mdc_when_python_in_languages() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        CursorAdapter.run(
            project_dir,
            layers={"universal": _UNIVERSAL, "python": _PYTHON},
            skills=_SKILLS,
        )

        assert (project_dir / ".cursor" / "rules" / "python.mdc").exists()


def test_no_python_mdc_when_python_absent() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        CursorAdapter.run(project_dir, layers={"universal": _UNIVERSAL}, skills=_SKILLS)

        assert not (project_dir / ".cursor" / "rules" / "python.mdc").exists()


def test_python_mdc_frontmatter_always_apply() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        CursorAdapter.run(
            project_dir,
            layers={"universal": _UNIVERSAL, "python": _PYTHON},
            skills=_SKILLS,
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
            skills=_SKILLS,
        )

        text = (project_dir / ".cursor" / "rules" / "python.mdc").read_text(
            encoding="utf-8"
        )
        _, _, body = text.split("---", 2)
        assert _PYTHON.strip() in body


def test_deploys_all_skills() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        CursorAdapter.run(project_dir, layers={"universal": _UNIVERSAL}, skills=_SKILLS)

        for name in _SKILLS:
            assert (project_dir / ".cursor" / "skills" / name / "SKILL.md").exists(), (
                f"Missing .cursor/skills/{name}/SKILL.md"
            )


def test_skill_content_matches() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        CursorAdapter.run(project_dir, layers={"universal": _UNIVERSAL}, skills=_SKILLS)

        for name, files in _SKILLS.items():
            for inner, content in files.items():
                text = (project_dir / ".cursor" / "skills" / name / inner).read_text(
                    encoding="utf-8"
                )
                assert text == content


def test_deploys_supporting_files() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        CursorAdapter.run(project_dir, layers={"universal": _UNIVERSAL}, skills=_SKILLS)

        assert (
            project_dir
            / ".cursor"
            / "skills"
            / "test-driven-development"
            / "testing-anti-patterns.md"
        ).exists()


def test_deploys_context7_mcp_config() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        result = CursorAdapter.run(
            project_dir, layers={"universal": _UNIVERSAL}, skills=_SKILLS
        )

        mcp = project_dir / ".cursor" / "mcp.json"
        assert mcp.exists()
        data = json.loads(mcp.read_text(encoding="utf-8"))
        ctx = data["mcpServers"]["context7"]
        assert ctx["command"] == "npx"
        assert "type" not in ctx
        assert ".cursor/mcp.json" in result


def test_gitignore_not_touched() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        CursorAdapter.run(project_dir, layers={"universal": _UNIVERSAL}, skills=_SKILLS)

        assert not (project_dir / ".gitignore").exists()


def test_rerun_overwrites_cleanly() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)
        layers = {"universal": _UNIVERSAL, "python": _PYTHON}

        CursorAdapter.run(project_dir, layers=layers, skills=_SKILLS)
        paths = [project_dir / ".cursor" / "rules" / "python.mdc"] + [
            project_dir / ".cursor" / "skills" / name / "SKILL.md" for name in _SKILLS
        ]
        first = {str(p): p.read_bytes() for p in paths}

        CursorAdapter.run(project_dir, layers=layers, skills=_SKILLS)

        for p in paths:
            assert p.read_bytes() == first[str(p)]


def test_returns_written_paths_python() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        result = CursorAdapter.run(
            project_dir,
            layers={"universal": _UNIVERSAL, "python": _PYTHON},
            skills=_SKILLS,
        )

        assert "AGENTS.md" not in result
        assert ".cursor/rules/python.mdc" in result
        for name in _SKILLS:
            assert f".cursor/skills/{name}/SKILL.md" in result


def test_returns_written_paths_no_python() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        result = CursorAdapter.run(
            project_dir,
            layers={"universal": _UNIVERSAL},
            skills=_SKILLS,
        )

        assert "AGENTS.md" not in result
        assert ".cursor/rules/python.mdc" not in result
        for name in _SKILLS:
            assert f".cursor/skills/{name}/SKILL.md" in result
