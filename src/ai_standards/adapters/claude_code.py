from pathlib import Path


class ClaudeCodeAdapter:
    @staticmethod
    def run(project_dir: Path, layers: dict[str, str]) -> list[str]:
        parts = [layers["universal"]]
        for lang in sorted(k for k in layers if k != "universal"):
            parts.append(layers[lang])
        content = "\n\n".join(p.rstrip() for p in parts) + "\n"
        (project_dir / "CLAUDE.local.md").write_text(content, encoding="utf-8")
        return ["CLAUDE.local.md"]
