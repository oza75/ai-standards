from pathlib import Path
from typing import Any

import yaml

from ai_standards.adapters.copilot import REVIEWER_AGENT_TOOLS

CONTENT_DIR = Path(__file__).parent.parent.parent / "content"


def _parse_frontmatter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    return yaml.safe_load(parts[1]) or {}


def test_plan_task_skill_name_matches_folder() -> None:
    path = CONTENT_DIR / "cursor" / "skills" / "plan-task" / "SKILL.md"
    fm = _parse_frontmatter(path)
    assert fm.get("name") == "plan-task"


def test_review_skill_name_matches_folder() -> None:
    path = CONTENT_DIR / "cursor" / "skills" / "review" / "SKILL.md"
    fm = _parse_frontmatter(path)
    assert fm.get("name") == "review"


def test_skill_descriptions_present() -> None:
    for skill in ("plan-task", "review"):
        path = CONTENT_DIR / "cursor" / "skills" / skill / "SKILL.md"
        fm = _parse_frontmatter(path)
        assert fm.get("description"), f"{skill}/SKILL.md missing non-empty description"


def test_reviewer_agent_tools_are_verified_list() -> None:
    path = CONTENT_DIR / "copilot" / "agents" / "reviewer.agent.md"
    fm = _parse_frontmatter(path)
    assert fm.get("tools") == REVIEWER_AGENT_TOOLS


def test_review_prompt_has_name() -> None:
    path = CONTENT_DIR / "copilot" / "prompts" / "review.prompt.md"
    fm = _parse_frontmatter(path)
    assert fm.get("name"), "review.prompt.md missing non-empty name"


def test_all_content_files_are_utf8() -> None:
    for rel in (
        "cursor/skills/plan-task/SKILL.md",
        "cursor/skills/review/SKILL.md",
        "copilot/agents/reviewer.agent.md",
        "copilot/prompts/review.prompt.md",
    ):
        (CONTENT_DIR / rel).read_text(encoding="utf-8")
