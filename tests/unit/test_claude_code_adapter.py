import tempfile
from pathlib import Path

from ai_standards.adapters.claude_code import ClaudeCodeAdapter

_UNIVERSAL = "# Universal\n\nUniversal coding standards."
_PYTHON = "# Python\n\nPython-specific standards."


def test_creates_claude_local_md() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        ClaudeCodeAdapter.run(project_dir, {"universal": _UNIVERSAL})

        assert (project_dir / "CLAUDE.local.md").exists()


def test_claude_local_contains_universal() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        ClaudeCodeAdapter.run(project_dir, {"universal": _UNIVERSAL})

        content = (project_dir / "CLAUDE.local.md").read_text(encoding="utf-8")
        assert _UNIVERSAL in content


def test_claude_local_contains_language_layer() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        ClaudeCodeAdapter.run(project_dir, {"universal": _UNIVERSAL, "python": _PYTHON})

        content = (project_dir / "CLAUDE.local.md").read_text(encoding="utf-8")
        assert _PYTHON in content


def test_claude_local_universal_only_when_no_language() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        ClaudeCodeAdapter.run(project_dir, {"universal": _UNIVERSAL})

        content = (project_dir / "CLAUDE.local.md").read_text(encoding="utf-8")
        assert _UNIVERSAL in content
        assert _PYTHON not in content


def test_does_not_touch_committed_claude_md() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)
        committed = project_dir / "CLAUDE.md"
        committed.write_bytes(b"committed standards")

        ClaudeCodeAdapter.run(project_dir, {"universal": _UNIVERSAL, "python": _PYTHON})

        assert committed.read_bytes() == b"committed standards"


def test_gitignore_not_touched() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        ClaudeCodeAdapter.run(project_dir, {"universal": _UNIVERSAL})

        assert not (project_dir / ".gitignore").exists()


def test_rerun_overwrites_cleanly() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)
        layers = {"universal": _UNIVERSAL, "python": _PYTHON}

        ClaudeCodeAdapter.run(project_dir, layers)
        first = (project_dir / "CLAUDE.local.md").read_bytes()
        ClaudeCodeAdapter.run(project_dir, layers)
        second = (project_dir / "CLAUDE.local.md").read_bytes()

        assert first == second


def test_returns_written_paths() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        result = ClaudeCodeAdapter.run(project_dir, {"universal": _UNIVERSAL})

        assert result == ["CLAUDE.local.md"]


def test_layers_separated_by_exactly_one_blank_line() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)
        universal_with_newline = _UNIVERSAL + "\n"
        python_with_newline = _PYTHON + "\n"

        ClaudeCodeAdapter.run(
            project_dir,
            {"universal": universal_with_newline, "python": python_with_newline},
        )

        content = (project_dir / "CLAUDE.local.md").read_text(encoding="utf-8")
        boundary = content[content.index(_UNIVERSAL) + len(_UNIVERSAL) :]
        assert boundary.startswith("\n\n"), "layers must be separated by one blank line"
        assert not boundary.startswith("\n\n\n"), "must not be two blank lines"
