import tempfile
from pathlib import Path

from ai_standards.adapters.shared import SharedAdapter

_UNIVERSAL = "# Universal\n\nUniversal coding standards."
_PYTHON = "# Python\n\nPython-specific standards."


def test_writes_agents_md() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        SharedAdapter.run(project_dir, {"universal": _UNIVERSAL})

        assert (project_dir / "AGENTS.md").exists()


def test_agents_md_has_universal_content() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        SharedAdapter.run(project_dir, {"universal": _UNIVERSAL})

        content = (project_dir / "AGENTS.md").read_text(encoding="utf-8")
        assert _UNIVERSAL in content


def test_agents_md_excludes_language_layers() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        SharedAdapter.run(project_dir, {"universal": _UNIVERSAL, "python": _PYTHON})

        content = (project_dir / "AGENTS.md").read_text(encoding="utf-8")
        assert _PYTHON not in content


def test_returns_agents_md_path() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        result = SharedAdapter.run(project_dir, {"universal": _UNIVERSAL})

        assert result == ["AGENTS.md"]


def test_gitignore_not_touched() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        SharedAdapter.run(project_dir, {"universal": _UNIVERSAL})

        assert not (project_dir / ".gitignore").exists()


def test_rerun_overwrites_cleanly() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        SharedAdapter.run(project_dir, {"universal": _UNIVERSAL})
        first = (project_dir / "AGENTS.md").read_bytes()
        SharedAdapter.run(project_dir, {"universal": _UNIVERSAL})
        second = (project_dir / "AGENTS.md").read_bytes()

        assert first == second
