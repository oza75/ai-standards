import tempfile
from pathlib import Path

from ai_standards.adapters.claude_code import ClaudeCodeAdapter

_UNIVERSAL = "# Universal\n\nUniversal coding standards."
_PYTHON = "# Python\n\nPython-specific standards."
_SKILLS = {
    "test-driven-development": {
        "SKILL.md": (
            "---\nname: test-driven-development\ndescription: TDD.\n---\n\n# TDD\n"
        ),
        "testing-anti-patterns.md": "# Testing anti-patterns\n\nDo not test mocks.\n",
    },
    "review": {
        "SKILL.md": "---\nname: review\ndescription: Review code.\n---\n\n# Review\n",
    },
}
_REVIEWER_AGENT = (
    "---\nname: reviewer\ntools: Read, Grep, Glob, Bash\n"
    "model: claude-opus-4-8\nskills: review\n---\n\n# reviewer\n"
)


def test_does_not_write_agents_md() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        ClaudeCodeAdapter.run(project_dir, {"universal": _UNIVERSAL}, _SKILLS)

        assert not (project_dir / "AGENTS.md").exists()


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


def test_deploys_skills_as_model_invocable_skills() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        ClaudeCodeAdapter.run(project_dir, {"universal": _UNIVERSAL}, _SKILLS)

        for name in _SKILLS:
            assert (project_dir / ".claude" / "skills" / name / "SKILL.md").exists(), (
                f"Missing .claude/skills/{name}/SKILL.md"
            )


def test_does_not_deploy_to_commands() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        ClaudeCodeAdapter.run(project_dir, {"universal": _UNIVERSAL}, _SKILLS)

        assert not (project_dir / ".claude" / "commands").exists()


def test_skill_content_matches() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        ClaudeCodeAdapter.run(project_dir, {"universal": _UNIVERSAL}, _SKILLS)

        for name, files in _SKILLS.items():
            for inner, content in files.items():
                text = (project_dir / ".claude" / "skills" / name / inner).read_text(
                    encoding="utf-8"
                )
                assert text == content


def test_deploys_supporting_files() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        ClaudeCodeAdapter.run(project_dir, {"universal": _UNIVERSAL}, _SKILLS)

        assert (
            project_dir
            / ".claude"
            / "skills"
            / "test-driven-development"
            / "testing-anti-patterns.md"
        ).exists()


def test_returns_claude_local_and_skill_paths() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        result = ClaudeCodeAdapter.run(project_dir, {"universal": _UNIVERSAL}, _SKILLS)

        assert "AGENTS.md" not in result
        assert "CLAUDE.local.md" in result
        for name in _SKILLS:
            assert f".claude/skills/{name}/SKILL.md" in result


def test_deploys_reviewer_subagent() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        ClaudeCodeAdapter.run(
            project_dir,
            {"universal": _UNIVERSAL},
            _SKILLS,
            reviewer_agent=_REVIEWER_AGENT,
        )

        agent = project_dir / ".claude" / "agents" / "reviewer.md"
        assert agent.exists()
        assert agent.read_text(encoding="utf-8") == _REVIEWER_AGENT


def test_reviewer_subagent_in_return_paths() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        result = ClaudeCodeAdapter.run(
            project_dir,
            {"universal": _UNIVERSAL},
            _SKILLS,
            reviewer_agent=_REVIEWER_AGENT,
        )

        assert ".claude/agents/reviewer.md" in result


def test_no_reviewer_subagent_when_omitted() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        ClaudeCodeAdapter.run(project_dir, {"universal": _UNIVERSAL}, _SKILLS)

        assert not (project_dir / ".claude" / "agents").exists()


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
        claude_first = (project_dir / "CLAUDE.local.md").read_bytes()
        skill_first = (
            project_dir / ".claude" / "skills" / "review" / "SKILL.md"
        ).read_bytes()

        ClaudeCodeAdapter.run(project_dir, layers, _SKILLS)

        assert (project_dir / "CLAUDE.local.md").read_bytes() == claude_first
        assert (
            project_dir / ".claude" / "skills" / "review" / "SKILL.md"
        ).read_bytes() == skill_first
