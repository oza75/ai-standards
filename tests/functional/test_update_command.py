"""Functional tests for the update command."""

import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import typer

from ai_standards.commands.sync import run as sync_run
from ai_standards.commands.update import run
from ai_standards.manifest import Manifest

_TEST_MANIFEST = Manifest(
    files=[
        "layers/universal.md",
        "layers/python.md",
        "content/skills/plan-task/SKILL.md",
        "content/skills/review/SKILL.md",
        "content/skills/test-driven-development/SKILL.md",
        "content/skills/reviewer-loop/SKILL.md",
        "content/skills/verification-before-completion/SKILL.md",
        "content/skills/systematic-debugging/SKILL.md",
        "content/copilot/agents/reviewer.agent.md",
    ],
    repo_url="https://github.com/oza/ai-standards",
    version_ref="main",
)


def _write_manifest(path: Path, manifest: Manifest) -> None:
    path.write_text(
        json.dumps(
            {
                "repo_url": manifest.repo_url,
                "version_ref": manifest.version_ref,
                "files": manifest.files,
            }
        ),
        encoding="utf-8",
    )


def _make_store(store_dir: Path, content: bytes = b"original content") -> None:
    for rel in _TEST_MANIFEST.files:
        dest = store_dir / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(content)


def _http_mock(content: bytes) -> MagicMock:
    mock_client = MagicMock()
    mock_resp = MagicMock()
    mock_resp.raise_for_status.return_value = None
    mock_resp.content = content
    mock_client.__enter__ = MagicMock(return_value=mock_client)
    mock_client.__exit__ = MagicMock(return_value=False)
    mock_client.get = MagicMock(return_value=mock_resp)
    return mock_client


def test_update_redeploys_files() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        store_dir = tmp_path / ".ai-standards"
        project_dir = tmp_path / "project"
        project_dir.mkdir()
        manifest_path = tmp_path / "manifest.json"
        _write_manifest(manifest_path, _TEST_MANIFEST)

        _make_store(store_dir, b"old content")
        sync_run(project_dir, store_dir, manifest_path)

        before = (project_dir / "AGENTS.md").read_text(encoding="utf-8")
        assert "old content" in before

        updated = b"updated canonical content"
        with patch(
            "ai_standards.installer.httpx.Client",
            return_value=_http_mock(updated),
        ):
            run(project_dir, store_dir, manifest_path)

        after = (project_dir / "AGENTS.md").read_text(encoding="utf-8")
        assert "updated canonical content" in after


def test_update_network_failure_leaves_store_intact(
    capsys: pytest.CaptureFixture[str],
) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        store_dir = tmp_path / ".ai-standards"
        project_dir = tmp_path / "project"
        project_dir.mkdir()
        manifest_path = tmp_path / "manifest.json"
        _write_manifest(manifest_path, _TEST_MANIFEST)

        _make_store(store_dir, b"original store content")
        original_files = {
            rel: (store_dir / rel).read_bytes() for rel in _TEST_MANIFEST.files
        }

        mock_client = MagicMock()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_client.get.side_effect = Exception("network failure")

        with patch("ai_standards.installer.httpx.Client", return_value=mock_client):
            with pytest.raises(typer.Exit) as exc_info:
                run(project_dir, store_dir, manifest_path)

        assert exc_info.value.exit_code == 1
        captured = capsys.readouterr()
        assert captured.err

        for rel in _TEST_MANIFEST.files:
            assert (store_dir / rel).read_bytes() == original_files[rel]


def test_update_failure_does_not_corrupt_deployed_files() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        store_dir = tmp_path / ".ai-standards"
        project_dir = tmp_path / "project"
        project_dir.mkdir()
        manifest_path = tmp_path / "manifest.json"
        _write_manifest(manifest_path, _TEST_MANIFEST)

        _make_store(store_dir, b"initial content")
        sync_run(project_dir, store_dir, manifest_path)
        deployed_before = (project_dir / "CLAUDE.local.md").read_bytes()

        mock_client = MagicMock()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_client.get.side_effect = Exception("network failure")

        with patch("ai_standards.installer.httpx.Client", return_value=mock_client):
            with pytest.raises(typer.Exit):
                run(project_dir, store_dir, manifest_path)

        assert (project_dir / "CLAUDE.local.md").read_bytes() == deployed_before


def test_sync_still_works_after_failed_update() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        store_dir = tmp_path / ".ai-standards"
        project_dir = tmp_path / "project"
        project_dir.mkdir()
        manifest_path = tmp_path / "manifest.json"
        _write_manifest(manifest_path, _TEST_MANIFEST)

        _make_store(store_dir, b"prior canonical content")

        mock_client = MagicMock()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_client.get.side_effect = Exception("network failure")

        with patch("ai_standards.installer.httpx.Client", return_value=mock_client):
            with pytest.raises(typer.Exit):
                run(project_dir, store_dir, manifest_path)

        sync_run(project_dir, store_dir, manifest_path)

        content = (project_dir / "AGENTS.md").read_text(encoding="utf-8")
        assert "prior canonical content" in content
