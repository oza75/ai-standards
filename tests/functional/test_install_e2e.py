"""End-to-end install test — skipped unless SKIP_NETWORK_TESTS is unset."""

import os
import tempfile
from pathlib import Path

import pytest

from ai_standards.installer import Installer
from ai_standards.manifest import load_manifest

MANIFEST_PATH = Path(__file__).parent.parent.parent / "layers" / "manifest.json"


@pytest.mark.skipif(
    os.environ.get("SKIP_NETWORK_TESTS") == "1",
    reason="SKIP_NETWORK_TESTS=1",
)
def test_install_end_to_end() -> None:
    manifest = load_manifest(MANIFEST_PATH)
    with tempfile.TemporaryDirectory() as tmp:
        store_dir = Path(tmp) / ".ai-standards"
        Installer.run(manifest, store_dir)
        for rel in manifest.files:
            assert (store_dir / rel).exists(), f"Missing after install: {rel}"
