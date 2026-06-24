import tempfile
from pathlib import Path
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
