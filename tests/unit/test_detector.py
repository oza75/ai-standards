import json
import tempfile
from pathlib import Path

from ai_standards.detector import detect_languages


def _dir(**files: str) -> Path:
    tmp = tempfile.mkdtemp()
    for name, content in files.items():
        Path(tmp, name).write_text(content, encoding="utf-8")
    return Path(tmp)


def test_detects_python_from_pyproject() -> None:
    d = _dir(**{"pyproject.toml": "[project]\nname = 'x'"})
    assert detect_languages(d, set()) == {"python"}


def test_detects_python_from_setup_py() -> None:
    d = _dir(**{"setup.py": "from setuptools import setup; setup()"})
    assert detect_languages(d, set()) == {"python"}


def test_detects_typescript_from_package_json() -> None:
    pkg = json.dumps({"devDependencies": {"typescript": "^5.0"}})
    d = _dir(**{"package.json": pkg})
    assert detect_languages(d, set()) == {"typescript"}


def test_js_only_returns_empty() -> None:
    pkg = json.dumps({"dependencies": {"react": "^18"}})
    d = _dir(**{"package.json": pkg})
    assert detect_languages(d, set()) == set()


def test_detects_both() -> None:
    pkg = json.dumps({"dependencies": {"typescript": "^5.0"}})
    d = _dir(**{"pyproject.toml": "[project]", "package.json": pkg})
    assert detect_languages(d, set()) == {"python", "typescript"}


def test_neither_returns_empty() -> None:
    d = _dir()
    assert detect_languages(d, set()) == set()


def test_flag_replaces_detected_python() -> None:
    pkg = json.dumps({"devDependencies": {"typescript": "^5.0"}})
    d = _dir(**{"package.json": pkg})
    assert detect_languages(d, {"python"}) == {"python"}


def test_flag_replaces_detected_typescript() -> None:
    d = _dir(**{"pyproject.toml": "[project]"})
    assert detect_languages(d, {"typescript"}) == {"typescript"}


def test_both_flags() -> None:
    d = _dir()
    assert detect_languages(d, {"python", "typescript"}) == {"python", "typescript"}
