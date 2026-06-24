import json
from dataclasses import dataclass
from pathlib import Path


class ManifestError(Exception):
    pass


@dataclass(frozen=True)
class Manifest:
    files: list[str]
    repo_url: str
    version_ref: str


def load_manifest(path: Path) -> Manifest:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        raise ManifestError(f"Cannot read manifest at {path}: {exc}") from exc

    missing = [key for key in ("files", "repo_url", "version_ref") if key not in data]
    if missing:
        raise ManifestError(
            f"Manifest at {path} is missing required fields: {', '.join(missing)}"
        )

    files = data["files"]
    if not isinstance(files, list) or not all(isinstance(f, str) for f in files):
        raise ManifestError(f"Manifest 'files' must be a list of strings at {path}")
    for field in ("repo_url", "version_ref"):
        if not isinstance(data[field], str) or not data[field]:
            raise ManifestError(
                f"Manifest '{field}' must be a non-empty string at {path}"
            )

    return Manifest(
        files=files,
        repo_url=data["repo_url"],
        version_ref=data["version_ref"],
    )
