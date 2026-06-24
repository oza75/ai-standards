"""Functional tests for the sync command."""

import tempfile
from pathlib import Path

import pytest
import typer

from ai_standards.commands.sync import run

REPO_ROOT = Path(__file__).parent.parent.parent
STORE_DIR = REPO_ROOT
MANIFEST_PATH = REPO_ROOT / "layers" / "manifest.json"


def test_sync_restores_mutated_file() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)
        (project_dir / "pyproject.toml").write_text(
            "[project]\nname = 'test'\n", encoding="utf-8"
        )

        run(project_dir, STORE_DIR, MANIFEST_PATH)
        original = (project_dir / "CLAUDE.local.md").read_bytes()

        (project_dir / "CLAUDE.local.md").write_bytes(b"mutated content")

        run(project_dir, STORE_DIR, MANIFEST_PATH)

        assert (project_dir / "CLAUDE.local.md").read_bytes() == original


def test_sync_not_installed_error(capsys: pytest.CaptureFixture[str]) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)
        non_existent = project_dir / ".ai-standards"

        with pytest.raises(typer.Exit) as exc_info:
            run(project_dir, non_existent, MANIFEST_PATH)

        assert exc_info.value.exit_code == 1
        captured = capsys.readouterr()
        assert "ai-standards install" in captured.err


def test_sync_does_not_touch_gitignore() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)
        gitignore = project_dir / ".gitignore"
        gitignore.write_text("*.pyc\n", encoding="utf-8")
        before = gitignore.read_bytes()

        run(project_dir, STORE_DIR, MANIFEST_PATH)

        assert gitignore.read_bytes() == before
