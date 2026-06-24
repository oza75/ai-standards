import tempfile
from pathlib import Path

import yaml

from ai_standards.adapters.copilot import REVIEWER_AGENT_TOOLS, CopilotAdapter

_UNIVERSAL = "# Universal\n\nUniversal coding standards.\n"
_REVIEWER_AGENT = (
    "---\nname: reviewer\ntools:\n  - read\n  - search\n---\n\n# Reviewer\n"
)
_SKILLS = {
    "review": {
        "SKILL.md": (
            "---\nname: review\ndescription: Review code.\n---\n\n# Code Review\n"
        ),
    },
    "test-driven-development": {
        "SKILL.md": (
            "---\nname: test-driven-development\ndescription: TDD.\n---\n\n# TDD\n"
        ),
        "testing-anti-patterns.md": "# Testing anti-patterns\n\nDo not test mocks.\n",
    },
}


def test_creates_copilot_instructions() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        CopilotAdapter.run(
            project_dir,
            layers={"universal": _UNIVERSAL},
            reviewer_agent=_REVIEWER_AGENT,
            skills=_SKILLS,
        )

        assert (project_dir / ".github" / "copilot-instructions.md").exists()


def test_copilot_instructions_has_universal_content() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        CopilotAdapter.run(
            project_dir,
            layers={"universal": _UNIVERSAL},
            reviewer_agent=_REVIEWER_AGENT,
            skills=_SKILLS,
        )

        content = (project_dir / ".github" / "copilot-instructions.md").read_text(
            encoding="utf-8"
        )
        assert _UNIVERSAL in content


def test_creates_reviewer_agent() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        CopilotAdapter.run(
            project_dir,
            layers={"universal": _UNIVERSAL},
            reviewer_agent=_REVIEWER_AGENT,
            skills=_SKILLS,
        )

        assert (project_dir / ".github" / "agents" / "reviewer.agent.md").exists()


def test_reviewer_agent_tools_are_verified_list() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        CopilotAdapter.run(
            project_dir,
            layers={"universal": _UNIVERSAL},
            reviewer_agent=_REVIEWER_AGENT,
            skills=_SKILLS,
        )

        text = (project_dir / ".github" / "agents" / "reviewer.agent.md").read_text(
            encoding="utf-8"
        )
        _, fm_text, _ = text.split("---", 2)
        fm = yaml.safe_load(fm_text)
        assert fm["tools"] == REVIEWER_AGENT_TOOLS


def test_reviewer_agent_has_persona_body() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        CopilotAdapter.run(
            project_dir,
            layers={"universal": _UNIVERSAL},
            reviewer_agent=_REVIEWER_AGENT,
            skills=_SKILLS,
        )

        text = (project_dir / ".github" / "agents" / "reviewer.agent.md").read_text(
            encoding="utf-8"
        )
        _, _, body = text.split("---", 2)
        assert body.strip()


def test_deploys_all_skills() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        CopilotAdapter.run(
            project_dir,
            layers={"universal": _UNIVERSAL},
            reviewer_agent=_REVIEWER_AGENT,
            skills=_SKILLS,
        )

        for name in _SKILLS:
            assert (project_dir / ".github" / "skills" / name / "SKILL.md").exists(), (
                f"Missing .github/skills/{name}/SKILL.md"
            )


def test_skill_content_matches() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        CopilotAdapter.run(
            project_dir,
            layers={"universal": _UNIVERSAL},
            reviewer_agent=_REVIEWER_AGENT,
            skills=_SKILLS,
        )

        for name, files in _SKILLS.items():
            for inner, content in files.items():
                text = (project_dir / ".github" / "skills" / name / inner).read_text(
                    encoding="utf-8"
                )
                assert text == content


def test_deploys_supporting_files() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        CopilotAdapter.run(
            project_dir,
            layers={"universal": _UNIVERSAL},
            reviewer_agent=_REVIEWER_AGENT,
            skills=_SKILLS,
        )

        assert (
            project_dir
            / ".github"
            / "skills"
            / "test-driven-development"
            / "testing-anti-patterns.md"
        ).exists()


def test_gitignore_not_touched() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        CopilotAdapter.run(
            project_dir,
            layers={"universal": _UNIVERSAL},
            reviewer_agent=_REVIEWER_AGENT,
            skills=_SKILLS,
        )

        assert not (project_dir / ".gitignore").exists()


def test_rerun_overwrites_cleanly() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        CopilotAdapter.run(
            project_dir,
            layers={"universal": _UNIVERSAL},
            reviewer_agent=_REVIEWER_AGENT,
            skills=_SKILLS,
        )
        paths = [
            project_dir / ".github" / "copilot-instructions.md",
            project_dir / ".github" / "agents" / "reviewer.agent.md",
        ] + [project_dir / ".github" / "skills" / name / "SKILL.md" for name in _SKILLS]
        first = {str(p): p.read_bytes() for p in paths}

        CopilotAdapter.run(
            project_dir,
            layers={"universal": _UNIVERSAL},
            reviewer_agent=_REVIEWER_AGENT,
            skills=_SKILLS,
        )

        for p in paths:
            assert p.read_bytes() == first[str(p)]


def test_returns_written_paths() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        result = CopilotAdapter.run(
            project_dir,
            layers={"universal": _UNIVERSAL},
            reviewer_agent=_REVIEWER_AGENT,
            skills=_SKILLS,
        )

        assert ".github/copilot-instructions.md" in result
        assert ".github/agents/reviewer.agent.md" in result
        for name in _SKILLS:
            assert f".github/skills/{name}/SKILL.md" in result
