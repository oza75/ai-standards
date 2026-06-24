"""Functional tests for the init command."""

import importlib.resources
import json
import tempfile
from pathlib import Path

import pytest
import typer

from ai_standards.commands.init import run

REPO_ROOT = Path(__file__).parent.parent.parent
STORE_DIR = REPO_ROOT
MANIFEST_PATH = REPO_ROOT / "layers" / "manifest.json"

_SKILL_NAMES = [
    "plan-task",
    "implement-story",
    "review",
    "test-driven-development",
    "reviewer-loop",
    "verification-before-completion",
    "systematic-debugging",
]

# Supporting (progressive-disclosure) files per skill, relative to the skill dir.
# These deploy to Claude Code and Cursor but NOT to Copilot (single .prompt.md).
_SUPPORTING_FILES = {
    "test-driven-development": ["testing-anti-patterns.md"],
    "systematic-debugging": ["root-cause-tracing.md", "defense-in-depth.md"],
}

# Every file within each skill, relative to the skill dir (SKILL.md + supporting).
_SKILL_INNER = {
    name: ["SKILL.md", *_SUPPORTING_FILES.get(name, [])] for name in _SKILL_NAMES
}

# Files that must exist on disk after init
_EXPECTED_DEPLOYED_FILES = (
    ["AGENTS.md", "CLAUDE.local.md", ".claude/agents/code-reviewer.md"]
    + [f".claude/skills/{n}/{f}" for n in _SKILL_NAMES for f in _SKILL_INNER[n]]
    + [f".cursor/skills/{n}/{f}" for n in _SKILL_NAMES for f in _SKILL_INNER[n]]
    + [".github/copilot-instructions.md", ".github/agents/reviewer.agent.md"]
    + [f".github/skills/{n}/{f}" for n in _SKILL_NAMES for f in _SKILL_INNER[n]]
)

# Entries that must appear in .gitignore
_EXPECTED_GITIGNORE_ENTRIES = (
    ["AGENTS.md", "CLAUDE.local.md", ".claude/agents/code-reviewer.md"]
    + [f".claude/skills/{n}/{f}" for n in _SKILL_NAMES for f in _SKILL_INNER[n]]
    + [f".cursor/skills/{n}/{f}" for n in _SKILL_NAMES for f in _SKILL_INNER[n]]
    + [".github/copilot-instructions.md", ".github/agents/reviewer.agent.md"]
    + [f".github/skills/{n}/{f}" for n in _SKILL_NAMES for f in _SKILL_INNER[n]]
)


def test_init_creates_all_adapter_files() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        run(project_dir, STORE_DIR, MANIFEST_PATH, set())

        for rel in _EXPECTED_DEPLOYED_FILES:
            assert (project_dir / rel).exists(), f"Missing: {rel}"


def test_init_gitignores_all_files() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        run(project_dir, STORE_DIR, MANIFEST_PATH, set())

        gitignore = (project_dir / ".gitignore").read_text(encoding="utf-8")
        for entry in _EXPECTED_GITIGNORE_ENTRIES:
            assert entry in gitignore, f".gitignore missing: {entry}"


def test_init_python_flag_forces_python_layer() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        run(project_dir, STORE_DIR, MANIFEST_PATH, {"python"})

        claude_local = (project_dir / "CLAUDE.local.md").read_text(encoding="utf-8")
        assert "## Typing" in claude_local, "CLAUDE.local.md missing Python layer"
        assert (project_dir / ".cursor" / "rules" / "python.mdc").exists()


def test_init_not_installed_error(capsys: pytest.CaptureFixture[str]) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)
        non_existent = project_dir / ".ai-standards"

        with pytest.raises(typer.Exit) as exc_info:
            run(project_dir, non_existent, MANIFEST_PATH, set())

        assert exc_info.value.exit_code == 1
        captured = capsys.readouterr()
        assert "ai-standards install" in captured.err


def test_init_typescript_warning(capsys: pytest.CaptureFixture[str]) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)
        pkg = {
            "name": "test",
            "dependencies": {"typescript": "^5.0.0"},
        }
        (project_dir / "package.json").write_text(json.dumps(pkg), encoding="utf-8")

        run(project_dir, STORE_DIR, MANIFEST_PATH, set())

        captured = capsys.readouterr()
        assert "no adapter" in captured.out
        assert (project_dir / "CLAUDE.local.md").exists()
        assert not (project_dir / ".cursor" / "rules" / "python.mdc").exists()


def test_init_idempotent() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        run(project_dir, STORE_DIR, MANIFEST_PATH, {"python"})
        files_first = {
            rel: (project_dir / rel).read_bytes() for rel in _EXPECTED_DEPLOYED_FILES
        }
        gitignore_first = (project_dir / ".gitignore").read_text(encoding="utf-8")

        run(project_dir, STORE_DIR, MANIFEST_PATH, {"python"})
        for rel in _EXPECTED_DEPLOYED_FILES:
            assert (project_dir / rel).read_bytes() == files_first[rel], (
                f"Content changed on re-run: {rel}"
            )
        gitignore_second = (project_dir / ".gitignore").read_text(encoding="utf-8")
        assert gitignore_first == gitignore_second, ".gitignore changed on re-run"


def test_bundled_manifest_matches_source_manifest() -> None:
    ref = importlib.resources.files("ai_standards") / "manifest.json"
    with importlib.resources.as_file(ref) as bundled:
        assert bundled.read_bytes() == MANIFEST_PATH.read_bytes()


def test_init_python_and_typescript_flags_together(
    capsys: pytest.CaptureFixture[str],
) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        run(project_dir, STORE_DIR, MANIFEST_PATH, {"python", "typescript"})

        captured = capsys.readouterr()
        assert "no adapter" in captured.out
        assert (project_dir / ".cursor" / "rules" / "python.mdc").exists()


def test_init_deploys_skills_to_all_three_tools() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        run(project_dir, STORE_DIR, MANIFEST_PATH, set())

        assert (
            project_dir / ".claude" / "skills" / "test-driven-development" / "SKILL.md"
        ).exists()
        assert (
            project_dir / ".cursor" / "skills" / "test-driven-development" / "SKILL.md"
        ).exists()
        assert (
            project_dir / ".github" / "skills" / "test-driven-development" / "SKILL.md"
        ).exists()
