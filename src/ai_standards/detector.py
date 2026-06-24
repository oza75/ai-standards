"""Language detection for a project directory.

Warnings for JS-only or no-language results are the responsibility of the
caller (init command, STD-11) — this module is a pure detection function.
"""

import json
from pathlib import Path


def detect_languages(project_dir: Path, flags: set[str]) -> set[str]:
    """Return the set of language keys for a project directory.

    If flags is non-empty, it replaces detection entirely.
    """
    if flags:
        return set(flags)

    detected: set[str] = set()

    if (project_dir / "pyproject.toml").exists() or (project_dir / "setup.py").exists():
        detected.add("python")

    pkg = project_dir / "package.json"
    if pkg.exists():
        try:
            data = json.loads(pkg.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            data = {}
        all_deps: dict[str, str] = {}
        all_deps.update(data.get("dependencies") or {})
        all_deps.update(data.get("devDependencies") or {})
        if "typescript" in all_deps:
            detected.add("typescript")

    return detected
