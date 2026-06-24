import tempfile
from pathlib import Path

import pytest

from ai_standards.store import CanonicalStore, NotInstalledError

MANIFEST_PATH = Path(__file__).parent.parent.parent / "layers" / "manifest.json"


def _make_store(files: dict[str, str]) -> tuple[CanonicalStore, Path]:
    """Build a fake ~/.ai-standards/ dir with given relative-path→content mapping."""
    tmp = Path(tempfile.mkdtemp())
    for rel, content in files.items():
        dest = tmp / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(content, encoding="utf-8")
    return CanonicalStore(tmp, MANIFEST_PATH), tmp


def _full_store_files() -> dict[str, str]:
    import json as _json

    manifest = _json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    return {f: f"content of {f}" for f in manifest["files"]}


def test_raises_not_installed_when_absent() -> None:
    missing = Path(tempfile.mkdtemp()) / "nonexistent"
    with pytest.raises(NotInstalledError, match="ai-standards install"):
        CanonicalStore(missing, MANIFEST_PATH)


def test_raises_on_incomplete_install() -> None:
    tmp = Path(tempfile.mkdtemp())
    tmp.mkdir(parents=True, exist_ok=True)
    # Only create one file instead of the full set
    (tmp / "layers").mkdir()
    (tmp / "layers" / "universal.md").write_text("x", encoding="utf-8")
    with pytest.raises(NotInstalledError, match="ai-standards install"):
        CanonicalStore(tmp, MANIFEST_PATH)


def test_assembles_universal_always() -> None:
    store, _ = _make_store(_full_store_files())
    layers = store.assemble_layers(set())
    assert "universal" in layers
    assert layers["universal"] == "content of layers/universal.md"


def test_assembles_python_layer() -> None:
    store, _ = _make_store(_full_store_files())
    layers = store.assemble_layers({"python"})
    assert "universal" in layers
    assert "python" in layers
    assert layers["python"] == "content of layers/python.md"


def test_get_content_returns_file_text() -> None:
    store, _ = _make_store(_full_store_files())
    text = store.get_content("content/skills/plan-task/SKILL.md")
    assert text == "content of content/skills/plan-task/SKILL.md"


def test_content_not_in_layer_dict() -> None:
    store, _ = _make_store(_full_store_files())
    layers = store.assemble_layers({"python", "typescript"})
    assert not any(k.startswith("content/") for k in layers)


def test_get_skills_returns_all_six() -> None:
    store, _ = _make_store(_full_store_files())
    skills = store.get_skills()
    expected = {
        "plan-task",
        "review",
        "test-driven-development",
        "reviewer-loop",
        "verification-before-completion",
        "systematic-debugging",
    }
    assert set(skills.keys()) == expected


def test_get_skills_values_are_nonempty_strings() -> None:
    store, _ = _make_store(_full_store_files())
    skills = store.get_skills()
    for name, content in skills.items():
        assert isinstance(content, str) and content, (
            f"skill {name!r} has empty or non-string content"
        )
