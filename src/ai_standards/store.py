from pathlib import Path

from ai_standards.manifest import Manifest, load_manifest

_LAYER_KEY = {
    "layers/universal.md": "universal",
    "layers/python.md": "python",
    "layers/typescript.md": "typescript",
}


class NotInstalledError(Exception):
    pass


class CanonicalStore:
    def __init__(self, store_dir: Path, manifest_path: Path) -> None:
        if not store_dir.exists():
            raise NotInstalledError(
                "~/.ai-standards/ not found. Run 'ai-standards install' first."
            )
        self._dir = store_dir
        self._manifest: Manifest = load_manifest(manifest_path)

        missing = [f for f in self._manifest.files if not (store_dir / f).exists()]
        if missing:
            raise NotInstalledError(
                f"Installation is incomplete (missing {len(missing)} file(s)). "
                "Run 'ai-standards install' to repair."
            )

    def assemble_layers(self, languages: set[str]) -> dict[str, str]:
        result: dict[str, str] = {}
        result["universal"] = (self._dir / "layers" / "universal.md").read_text(
            encoding="utf-8"
        )
        for lang in languages:
            key = f"layers/{lang}.md"
            if key in _LAYER_KEY:
                result[lang] = (self._dir / key).read_text(encoding="utf-8")
        return result

    def get_content(self, relative_path: str) -> str:
        if not relative_path.startswith("content/"):
            raise ValueError(
                f"get_content path must start with 'content/': {relative_path!r}"
            )
        return (self._dir / relative_path).read_text(encoding="utf-8")

    def get_skills(self) -> dict[str, dict[str, str]]:
        """Return every shared skill as {skill_name: {path_within_skill: content}}.

        A skill is a directory under `content/skills/<name>/`; it always has a
        `SKILL.md` and may carry supporting files (e.g. `testing-anti-patterns.md`)
        for progressive disclosure. The inner key is the path relative to the
        skill directory, so nested supporting files keep their structure.
        """
        result: dict[str, dict[str, str]] = {}
        for rel in self._manifest.files:
            parts = rel.split("/")
            if len(parts) >= 4 and parts[0] == "content" and parts[1] == "skills":
                skill_name = parts[2]
                inner_path = "/".join(parts[3:])
                result.setdefault(skill_name, {})[inner_path] = (
                    self._dir / rel
                ).read_text(encoding="utf-8")
        return result
