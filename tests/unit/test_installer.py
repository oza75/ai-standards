import tempfile
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from ai_standards.installer import Installer
from ai_standards.manifest import Manifest

MANIFEST = Manifest(
    files=["layers/universal.md", "layers/python.md"],
    repo_url="https://github.com/oza/ai-standards",
    version_ref="main",
)

_RAW_URL = "https://raw.githubusercontent.com/oza/ai-standards/main/{path}"


def _make_http_mock(content: bytes = b"fake content") -> MagicMock:
    mock_client = MagicMock()
    mock_resp = MagicMock()
    mock_resp.raise_for_status.return_value = None
    mock_resp.content = content
    mock_client.__enter__ = MagicMock(return_value=mock_client)
    mock_client.__exit__ = MagicMock(return_value=False)
    mock_client.get = MagicMock(return_value=mock_resp)
    return mock_client


def test_downloads_all_manifest_files() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        store_dir = Path(tmp) / ".ai-standards"
        mock_client = _make_http_mock(b"content")
        with patch("ai_standards.installer.httpx.Client", return_value=mock_client):
            Installer.run(MANIFEST, store_dir)
        for rel in MANIFEST.files:
            assert (store_dir / rel).exists(), f"Missing: {rel}"


def test_second_run_is_idempotent() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        store_dir = Path(tmp) / ".ai-standards"
        mock_client = _make_http_mock(b"fixed content")
        with patch("ai_standards.installer.httpx.Client", return_value=mock_client):
            Installer.run(MANIFEST, store_dir)
        files_after_first = {
            rel: (store_dir / rel).read_bytes() for rel in MANIFEST.files
        }
        with patch("ai_standards.installer.httpx.Client", return_value=mock_client):
            Installer.run(MANIFEST, store_dir)
        for rel in MANIFEST.files:
            assert (store_dir / rel).read_bytes() == files_after_first[rel]


def test_partial_download_leaves_live_unchanged() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        store_dir = Path(tmp) / ".ai-standards"
        # Pre-populate live dir
        (store_dir / "layers").mkdir(parents=True)
        (store_dir / "layers" / "universal.md").write_text("original", encoding="utf-8")

        call_count = 0

        def failing_get(url: str, **kwargs: object) -> MagicMock:
            nonlocal call_count
            call_count += 1
            if call_count > 1:
                import httpx

                raise httpx.RequestError("network failure")
            resp = MagicMock()
            resp.raise_for_status.return_value = None
            resp.content = b"new content"
            return resp

        mock_client = MagicMock()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_client.get = failing_get

        with patch("ai_standards.installer.httpx.Client", return_value=mock_client):
            with pytest.raises(Exception):
                Installer.run(MANIFEST, store_dir)

        universal = store_dir / "layers" / "universal.md"
        assert universal.read_text(encoding="utf-8") == "original"


def test_first_install_leaves_live_absent_on_failure() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        store_dir = Path(tmp) / ".ai-standards"

        mock_client = MagicMock()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_client.get.side_effect = Exception("network failure")

        with patch("ai_standards.installer.httpx.Client", return_value=mock_client):
            with pytest.raises(Exception):
                Installer.run(MANIFEST, store_dir)

        assert not store_dir.exists()


def test_staging_cleaned_on_failure() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        store_dir = Path(tmp) / ".ai-standards"
        staging = Path(str(store_dir) + ".staging")

        mock_client = MagicMock()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_client.get.side_effect = Exception("boom")

        with patch("ai_standards.installer.httpx.Client", return_value=mock_client):
            with pytest.raises(Exception):
                Installer.run(MANIFEST, store_dir)

        assert not staging.exists()


def test_all_expected_files_present_after_success() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        store_dir = Path(tmp) / ".ai-standards"
        mock_client = _make_http_mock(b"data")
        with patch("ai_standards.installer.httpx.Client", return_value=mock_client):
            Installer.run(MANIFEST, store_dir)
        for rel in MANIFEST.files:
            assert (store_dir / rel).exists()


def test_rename_failure_rolls_back_store_dir() -> None:
    """If staging.rename(store_dir) raises, original store_dir is restored."""
    with tempfile.TemporaryDirectory() as tmp:
        store_dir = Path(tmp) / ".ai-standards"
        (store_dir / "layers").mkdir(parents=True)
        (store_dir / "layers" / "universal.md").write_bytes(b"original")

        original_rename = Path.rename
        rename_calls: list[Any] = []

        def tracked_rename(self: Path, target: Path) -> Path:
            rename_calls.append(self)
            if len(rename_calls) == 2:
                raise OSError("simulated rename failure")
            return original_rename(self, target)

        mock_client = _make_http_mock(b"new content")
        with patch("ai_standards.installer.httpx.Client", return_value=mock_client):
            with patch.object(Path, "rename", tracked_rename):
                with pytest.raises(OSError):
                    Installer.run(MANIFEST, store_dir)

        assert (store_dir / "layers" / "universal.md").read_bytes() == b"original"
        assert not Path(str(store_dir) + ".old").exists()
        assert not Path(str(store_dir) + ".staging").exists()


def test_recovery_from_crashed_rename_phase() -> None:
    """If a prior run left old_dir but no store_dir, the next run recovers."""
    with tempfile.TemporaryDirectory() as tmp:
        store_dir = Path(tmp) / ".ai-standards"
        old_dir = Path(str(store_dir) + ".old")

        # Simulate crashed state: old_dir has prior canonical, store_dir is absent
        (old_dir / "layers").mkdir(parents=True)
        (old_dir / "layers" / "universal.md").write_bytes(b"prior content")

        mock_client = _make_http_mock(b"new content")
        with patch("ai_standards.installer.httpx.Client", return_value=mock_client):
            Installer.run(MANIFEST, store_dir)

        assert (store_dir / "layers" / "universal.md").read_bytes() == b"new content"
        assert not old_dir.exists()


def test_recovery_prefers_complete_staging_when_both_staging_and_old_exist() -> None:
    """If old_dir + staging both present without store_dir, staging is promoted."""
    with tempfile.TemporaryDirectory() as tmp:
        store_dir = Path(tmp) / ".ai-standards"
        old_dir = Path(str(store_dir) + ".old")
        staging_dir = Path(str(store_dir) + ".staging")

        (old_dir / "layers").mkdir(parents=True)
        (old_dir / "layers" / "universal.md").write_bytes(b"prior content")
        (staging_dir / "layers").mkdir(parents=True)
        (staging_dir / "layers" / "universal.md").write_bytes(b"staged content")

        mock_client = _make_http_mock(b"fresh content")
        with patch("ai_standards.installer.httpx.Client", return_value=mock_client):
            Installer.run(MANIFEST, store_dir)

        assert (store_dir / "layers" / "universal.md").read_bytes() == b"fresh content"
        assert not old_dir.exists()
        assert not staging_dir.exists()


def test_first_rename_failure_cleans_staging() -> None:
    """If the first rename fails, store_dir is preserved and staging is cleaned."""
    with tempfile.TemporaryDirectory() as tmp:
        store_dir = Path(tmp) / ".ai-standards"
        (store_dir / "layers").mkdir(parents=True)
        (store_dir / "layers" / "universal.md").write_bytes(b"original")

        original_rename = Path.rename
        rename_calls: list[Any] = []

        def tracked_rename(self: Path, target: Path) -> Path:
            rename_calls.append(self)
            if len(rename_calls) == 1:
                raise OSError("simulated first rename failure")
            return original_rename(self, target)

        mock_client = _make_http_mock(b"new content")
        with patch("ai_standards.installer.httpx.Client", return_value=mock_client):
            with patch.object(Path, "rename", tracked_rename):
                with pytest.raises(OSError):
                    Installer.run(MANIFEST, store_dir)

        assert (store_dir / "layers" / "universal.md").read_bytes() == b"original"
        assert not Path(str(store_dir) + ".old").exists()
        assert not Path(str(store_dir) + ".staging").exists()
