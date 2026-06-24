import tempfile
from pathlib import Path

import yaml

from ai_standards.adapters.copilot import REVIEWER_AGENT_TOOLS, CopilotAdapter

_UNIVERSAL = "# Universal\n\nUniversal coding standards.\n"
_REVIEWER_AGENT = (
    "---\nname: reviewer\ntools:\n  - read\n  - search\n---\n\n# Reviewer\n"
)
_REVIEW_PROMPT = "---\nname: review\n---\n\n# Code Review\n"


def test_creates_copilot_instructions() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        CopilotAdapter.run(
            project_dir,
            layers={"universal": _UNIVERSAL},
            reviewer_agent=_REVIEWER_AGENT,
            review_prompt=_REVIEW_PROMPT,
        )

        assert (project_dir / ".github" / "copilot-instructions.md").exists()


def test_copilot_instructions_has_universal_content() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        CopilotAdapter.run(
            project_dir,
            layers={"universal": _UNIVERSAL},
            reviewer_agent=_REVIEWER_AGENT,
            review_prompt=_REVIEW_PROMPT,
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
            review_prompt=_REVIEW_PROMPT,
        )

        assert (project_dir / ".github" / "agents" / "reviewer.agent.md").exists()


def test_reviewer_agent_tools_are_verified_list() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        CopilotAdapter.run(
            project_dir,
            layers={"universal": _UNIVERSAL},
            reviewer_agent=_REVIEWER_AGENT,
            review_prompt=_REVIEW_PROMPT,
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
            review_prompt=_REVIEW_PROMPT,
        )

        text = (project_dir / ".github" / "agents" / "reviewer.agent.md").read_text(
            encoding="utf-8"
        )
        _, _, body = text.split("---", 2)
        assert body.strip()


def test_creates_review_prompt() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        CopilotAdapter.run(
            project_dir,
            layers={"universal": _UNIVERSAL},
            reviewer_agent=_REVIEWER_AGENT,
            review_prompt=_REVIEW_PROMPT,
        )

        assert (project_dir / ".github" / "prompts" / "review.prompt.md").exists()


def test_review_prompt_has_name() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        CopilotAdapter.run(
            project_dir,
            layers={"universal": _UNIVERSAL},
            reviewer_agent=_REVIEWER_AGENT,
            review_prompt=_REVIEW_PROMPT,
        )

        text = (project_dir / ".github" / "prompts" / "review.prompt.md").read_text(
            encoding="utf-8"
        )
        _, fm_text, _ = text.split("---", 2)
        fm = yaml.safe_load(fm_text)
        assert fm.get("name") and isinstance(fm["name"], str)


def test_gitignore_not_touched() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        CopilotAdapter.run(
            project_dir,
            layers={"universal": _UNIVERSAL},
            reviewer_agent=_REVIEWER_AGENT,
            review_prompt=_REVIEW_PROMPT,
        )

        assert not (project_dir / ".gitignore").exists()


def test_rerun_overwrites_cleanly() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        CopilotAdapter.run(
            project_dir,
            layers={"universal": _UNIVERSAL},
            reviewer_agent=_REVIEWER_AGENT,
            review_prompt=_REVIEW_PROMPT,
        )
        paths = [
            project_dir / ".github" / "copilot-instructions.md",
            project_dir / ".github" / "agents" / "reviewer.agent.md",
            project_dir / ".github" / "prompts" / "review.prompt.md",
        ]
        first = {str(p): p.read_bytes() for p in paths}

        CopilotAdapter.run(
            project_dir,
            layers={"universal": _UNIVERSAL},
            reviewer_agent=_REVIEWER_AGENT,
            review_prompt=_REVIEW_PROMPT,
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
            review_prompt=_REVIEW_PROMPT,
        )

        assert len(result) == 3
        assert ".github/copilot-instructions.md" in result
        assert ".github/agents/reviewer.agent.md" in result
        assert ".github/prompts/review.prompt.md" in result
