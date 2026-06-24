import tempfile
from pathlib import Path

from ai_standards.gitignore import GitignoreManager

BEGIN = "# BEGIN ai-standards"
END = "# END ai-standards"


def _tmpfile(content: str = "") -> Path:
    f = tempfile.NamedTemporaryFile(mode="w", suffix=".gitignore", delete=False)
    f.write(content)
    f.close()
    return Path(f.name)


def test_inserts_managed_block() -> None:
    p = _tmpfile()
    GitignoreManager.add_paths(p, ["CLAUDE.local.md", "AGENTS.md"])
    text = p.read_text(encoding="utf-8")
    assert BEGIN in text
    assert END in text
    assert "CLAUDE.local.md" in text
    assert "AGENTS.md" in text


def test_idempotent_same_paths() -> None:
    p = _tmpfile()
    GitignoreManager.add_paths(p, ["CLAUDE.local.md"])
    first = p.read_text(encoding="utf-8")
    GitignoreManager.add_paths(p, ["CLAUDE.local.md"])
    second = p.read_text(encoding="utf-8")
    assert first == second


def test_replaces_block_with_new_paths() -> None:
    p = _tmpfile("# existing\n")
    GitignoreManager.add_paths(p, ["old.md"])
    GitignoreManager.add_paths(p, ["new.md"])
    text = p.read_text(encoding="utf-8")
    assert "# existing" in text
    assert "new.md" in text
    assert "old.md" not in text


def test_creates_gitignore_if_absent() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / ".gitignore"
        assert not p.exists()
        GitignoreManager.add_paths(p, ["CLAUDE.local.md"])
        assert p.exists()
        assert "CLAUDE.local.md" in p.read_text(encoding="utf-8")


def test_remove_block_deletes_block() -> None:
    p = _tmpfile("# other\n")
    GitignoreManager.add_paths(p, ["CLAUDE.local.md"])
    GitignoreManager.remove_block(p)
    text = p.read_text(encoding="utf-8")
    assert BEGIN not in text
    assert END not in text
    assert "# other" in text


def test_idempotent_with_trailing_content() -> None:
    p = _tmpfile("# above\n")
    GitignoreManager.add_paths(p, ["CLAUDE.local.md"])
    # Append content after the managed block
    p.write_text(p.read_text(encoding="utf-8") + "# below\n", encoding="utf-8")
    first = p.read_text(encoding="utf-8")
    GitignoreManager.add_paths(p, ["CLAUDE.local.md"])
    second = p.read_text(encoding="utf-8")
    assert first == second


def test_preserves_content_after_block() -> None:
    p = _tmpfile("# above\n")
    GitignoreManager.add_paths(p, ["CLAUDE.local.md"])
    p.write_text(p.read_text(encoding="utf-8") + "# below\n", encoding="utf-8")
    GitignoreManager.add_paths(p, ["AGENTS.md"])
    text = p.read_text(encoding="utf-8")
    assert "# above" in text
    assert "# below" in text
    assert "AGENTS.md" in text
    assert "CLAUDE.local.md" not in text


def test_remove_block_noop_when_absent() -> None:
    p = _tmpfile("# unrelated\n")
    before = p.read_text(encoding="utf-8")
    GitignoreManager.remove_block(p)
    after = p.read_text(encoding="utf-8")
    assert before == after
