from pathlib import Path

LAYERS_DIR = Path(__file__).parent.parent.parent / "layers"


def test_universal_has_required_sections() -> None:
    text = (LAYERS_DIR / "universal.md").read_text(encoding="utf-8")
    for heading in ("## Naming", "## Docs", "## Tests", "## Git"):
        assert heading in text, f"universal.md missing section: {heading}"


def test_python_has_required_sections() -> None:
    text = (LAYERS_DIR / "python.md").read_text(encoding="utf-8")
    for heading in ("## Typing", "## Async-Sync", "## Tools"):
        assert heading in text, f"python.md missing section: {heading}"


def test_python_sections_absent_from_universal() -> None:
    text = (LAYERS_DIR / "universal.md").read_text(encoding="utf-8")
    for heading in ("## Typing", "## Async-Sync", "## Tools"):
        assert heading not in text, f"universal.md should not contain: {heading}"


def test_typescript_has_required_sections() -> None:
    text = (LAYERS_DIR / "typescript.md").read_text(encoding="utf-8")
    for heading in ("## Naming", "## Typing", "## Tests"):
        assert heading in text, f"typescript.md missing section: {heading}"


def test_typescript_marked_as_stub() -> None:
    text = (LAYERS_DIR / "typescript.md").read_text(encoding="utf-8")
    assert "stub" in text.lower(), "typescript.md must be marked as a stub"


def test_all_layer_files_are_utf8() -> None:
    for name in ("universal.md", "python.md", "typescript.md"):
        (LAYERS_DIR / name).read_text(encoding="utf-8")
