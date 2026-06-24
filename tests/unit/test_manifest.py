import json
import tempfile
from pathlib import Path

import pytest

from ai_standards.manifest import ManifestError, load_manifest

MANIFEST_PATH = Path(__file__).parent.parent.parent / "layers" / "manifest.json"


def test_manifest_is_valid_json() -> None:
    json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def test_manifest_has_files_list() -> None:
    m = load_manifest(MANIFEST_PATH)
    assert isinstance(m.files, list)
    assert len(m.files) > 0
    assert all(isinstance(f, str) for f in m.files)


def test_manifest_lists_all_layer_files() -> None:
    m = load_manifest(MANIFEST_PATH)
    for expected in ("layers/universal.md", "layers/python.md", "layers/typescript.md"):
        assert expected in m.files, f"manifest missing: {expected}"


def test_manifest_lists_all_content_files() -> None:
    m = load_manifest(MANIFEST_PATH)
    for expected in (
        "content/skills/plan-task/SKILL.md",
        "content/skills/review/SKILL.md",
        "content/skills/test-driven-development/SKILL.md",
        "content/skills/reviewer-loop/SKILL.md",
        "content/skills/verification-before-completion/SKILL.md",
        "content/skills/systematic-debugging/SKILL.md",
        "content/skills/implement-story/SKILL.md",
        "content/claude/agents/reviewer.md",
        "content/copilot/agents/reviewer.agent.md",
    ):
        assert expected in m.files, f"manifest missing: {expected}"


def test_manifest_has_repo_url() -> None:
    m = load_manifest(MANIFEST_PATH)
    assert isinstance(m.repo_url, str)
    assert m.repo_url


def test_manifest_has_version_ref() -> None:
    m = load_manifest(MANIFEST_PATH)
    assert isinstance(m.version_ref, str)
    assert m.version_ref


def test_manifest_loader_raises_on_missing_files_field() -> None:
    with tempfile.NamedTemporaryFile(suffix=".json", mode="w", delete=False) as f:
        json.dump({"repo_url": "https://example.com", "version_ref": "main"}, f)
        path = Path(f.name)
    with pytest.raises(ManifestError, match="files"):
        load_manifest(path)


def test_manifest_loader_raises_on_missing_repo_url() -> None:
    with tempfile.NamedTemporaryFile(suffix=".json", mode="w", delete=False) as f:
        json.dump({"files": ["layers/universal.md"], "version_ref": "main"}, f)
        path = Path(f.name)
    with pytest.raises(ManifestError, match="repo_url"):
        load_manifest(path)


def test_manifest_loader_raises_on_missing_version_ref() -> None:
    with tempfile.NamedTemporaryFile(suffix=".json", mode="w", delete=False) as f:
        json.dump(
            {"files": ["layers/universal.md"], "repo_url": "https://example.com"}, f
        )
        path = Path(f.name)
    with pytest.raises(ManifestError, match="version_ref"):
        load_manifest(path)
