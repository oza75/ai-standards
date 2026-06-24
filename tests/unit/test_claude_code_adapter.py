import tempfile
from pathlib import Path

from ai_standards.adapters.claude_code import ClaudeCodeAdapter

_UNIVERSAL = "# Universal\n\nUniversal coding standards."
_PYTHON = "# Python\n\nPython-specific standards."
_SKILLS = {
    "test-driven-development": (
        "---\nname: test-driven-development\ndescription: TDD.\n---\n\n# TDD\n"
    ),
    "review": "---\nname: review\ndescription: Review code.\n---\n\n# Review\n",
}


def test_writes_agents_md() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        ClaudeCodeAdapter.run(project_dir, {"universal": _UNIVERSAL}, _SKILLS)

        assert (project_dir / "AGENTS.md").exists()


def test_agents_md_has_universal_content() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        ClaudeCodeAdapter.run(project_dir, {"universal": _UNIVERSAL}, _SKILLS)

        content = (project_dir / "AGENTS.md").read_text(encoding="utf-8")
        assert _UNIVERSAL in content


def test_claude_local_starts_with_agents_import() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        ClaudeCodeAdapter.run(project_dir, {"universal": _UNIVERSAL}, _SKILLS)

        content = (project_dir / "CLAUDE.local.md").read_text(encoding="utf-8")
        assert content.startswith("@AGENTS.md")


def test_claude_local_does_not_contain_universal_inline() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        ClaudeCodeAdapter.run(project_dir, {"universal": _UNIVERSAL}, _SKILLS)

        content = (project_dir / "CLAUDE.local.md").read_text(encoding="utf-8")
        assert _UNIVERSAL not in content


def test_claude_local_contains_language_layer() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        ClaudeCodeAdapter.run(
            project_dir, {"universal": _UNIVERSAL, "python": _PYTHON}, _SKILLS
        )

        content = (project_dir / "CLAUDE.local.md").read_text(encoding="utf-8")
        assert _PYTHON in content


def test_claude_local_is_only_import_when_no_language() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        ClaudeCodeAdapter.run(project_dir, {"universal": _UNIVERSAL}, _SKILLS)

        content = (project_dir / "CLAUDE.local.md").read_text(encoding="utf-8")
        assert content.strip() == "@AGENTS.md"


def test_import_and_language_layer_separated_by_one_blank_line() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)
        python_with_newline = _PYTHON + "\n"

        ClaudeCodeAdapter.run(
            project_dir,
            {"universal": _UNIVERSAL, "python": python_with_newline},
            _SKILLS,
        )

        content = (project_dir / "CLAUDE.local.md").read_text(encoding="utf-8")
        after_import = content[len("@AGENTS.md") :]
        assert after_import.startswith("\n\n"), "must be one blank line"
        assert not after_import.startswith("\n\n\n"), "must not be two blank lines"


def test_deploys_commands_for_all_skills() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        ClaudeCodeAdapter.run(project_dir, {"universal": _UNIVERSAL}, _SKILLS)

        for name in _SKILLS:
            assert (project_dir / ".claude" / "commands" / f"{name}.md").exists()


def test_command_content_matches_skill() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        ClaudeCodeAdapter.run(project_dir, {"universal": _UNIVERSAL}, _SKILLS)

        for name, skill_content in _SKILLS.items():
            cmd = (project_dir / ".claude" / "commands" / f"{name}.md").read_text(
                encoding="utf-8"
            )
            assert cmd == skill_content


def test_returns_agents_md_and_commands_dir() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        result = ClaudeCodeAdapter.run(project_dir, {"universal": _UNIVERSAL}, _SKILLS)

        assert "AGENTS.md" in result
        assert "CLAUDE.local.md" in result
        assert ".claude/commands/" in result


def test_does_not_touch_committed_claude_md() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)
        committed = project_dir / "CLAUDE.md"
        committed.write_bytes(b"committed standards")

        ClaudeCodeAdapter.run(
            project_dir, {"universal": _UNIVERSAL, "python": _PYTHON}, _SKILLS
        )

        assert committed.read_bytes() == b"committed standards"


def test_gitignore_not_touched() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        ClaudeCodeAdapter.run(project_dir, {"universal": _UNIVERSAL}, _SKILLS)

        assert not (project_dir / ".gitignore").exists()


def test_rerun_overwrites_cleanly() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)
        layers = {"universal": _UNIVERSAL, "python": _PYTHON}

        ClaudeCodeAdapter.run(project_dir, layers, _SKILLS)
        agents_first = (project_dir / "AGENTS.md").read_bytes()
        claude_first = (project_dir / "CLAUDE.local.md").read_bytes()

        ClaudeCodeAdapter.run(project_dir, layers, _SKILLS)

        assert (project_dir / "AGENTS.md").read_bytes() == agents_first
        assert (project_dir / "CLAUDE.local.md").read_bytes() == claude_first
