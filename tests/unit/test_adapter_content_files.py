from pathlib import Path
from typing import Any

import yaml

from ai_standards.adapters.copilot import REVIEWER_AGENT_TOOLS

CONTENT_DIR = Path(__file__).parent.parent.parent / "content"
LAYERS_DIR = Path(__file__).parent.parent.parent / "layers"
MANIFEST_PATH = LAYERS_DIR / "manifest.json"

SKILL_NAMES = [
    "plan-task",
    "implement-story",
    "review",
    "test-driven-development",
    "reviewer-loop",
    "verification-before-completion",
    "systematic-debugging",
]


def _parse_frontmatter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    return yaml.safe_load(parts[1]) or {}


def test_all_six_skill_files_exist() -> None:
    for name in SKILL_NAMES:
        path = CONTENT_DIR / "skills" / name / "SKILL.md"
        assert path.exists(), f"Missing: content/skills/{name}/SKILL.md"


def test_skill_name_matches_directory() -> None:
    for name in SKILL_NAMES:
        path = CONTENT_DIR / "skills" / name / "SKILL.md"
        fm = _parse_frontmatter(path)
        assert fm.get("name") == name, (
            f"content/skills/{name}/SKILL.md: "
            f"frontmatter name={fm.get('name')!r}, expected {name!r}"
        )


def test_skill_descriptions_present() -> None:
    for name in SKILL_NAMES:
        path = CONTENT_DIR / "skills" / name / "SKILL.md"
        fm = _parse_frontmatter(path)
        assert fm.get("description"), (
            f"content/skills/{name}/SKILL.md missing non-empty description"
        )


def test_workflow_section_references_all_skill_names() -> None:
    universal = (LAYERS_DIR / "universal.md").read_text(encoding="utf-8")
    assert "## Workflow" in universal, "universal.md missing Workflow section"
    for name in SKILL_NAMES:
        assert name in universal, (
            f"Workflow section in universal.md does not reference skill {name!r}"
        )


def test_manifest_paths_match_actual_files() -> None:
    import json

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    manifest_skill_paths = {
        p for p in manifest["files"] if p.startswith("content/skills/")
    }
    disk_skill_paths = {
        "content/skills/" + p.relative_to(CONTENT_DIR / "skills").as_posix()
        for p in (CONTENT_DIR / "skills").rglob("*")
        if p.is_file()
    }
    assert manifest_skill_paths == disk_skill_paths, (
        f"Manifest and disk disagree.\n"
        f"  In manifest only: {manifest_skill_paths - disk_skill_paths}\n"
        f"  On disk only: {disk_skill_paths - manifest_skill_paths}"
    )


def test_reviewer_agent_tools_are_verified_list() -> None:
    path = CONTENT_DIR / "copilot" / "agents" / "reviewer.agent.md"
    fm = _parse_frontmatter(path)
    assert fm.get("tools") == REVIEWER_AGENT_TOOLS


def test_all_skill_files_are_utf8() -> None:
    for name in SKILL_NAMES:
        (CONTENT_DIR / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
    (CONTENT_DIR / "copilot" / "agents" / "reviewer.agent.md").read_text(
        encoding="utf-8"
    )
