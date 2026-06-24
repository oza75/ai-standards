import shutil
from pathlib import Path

import httpx

from ai_standards.manifest import Manifest

_RAW_URL = "https://raw.githubusercontent.com/{owner}/{repo}/{ref}/{path}"


def _raw_url(repo_url: str, version_ref: str, path: str) -> str:
    # repo_url: https://github.com/owner/repo
    parts = repo_url.rstrip("/").split("/")
    owner, repo = parts[-2], parts[-1]
    return _RAW_URL.format(owner=owner, repo=repo, ref=version_ref, path=path)


class Installer:
    @staticmethod
    def run(manifest: Manifest, store_dir: Path) -> None:
        staging = Path(str(store_dir) + ".staging")
        old_dir = Path(str(store_dir) + ".old")

        if staging.exists():
            shutil.rmtree(staging)

        try:
            with httpx.Client() as client:
                for rel in manifest.files:
                    dest = staging / rel
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    url = _raw_url(manifest.repo_url, manifest.version_ref, rel)
                    resp = client.get(url)
                    resp.raise_for_status()
                    dest.write_bytes(resp.content)
        except Exception:
            shutil.rmtree(staging, ignore_errors=True)
            raise

        if store_dir.exists():
            store_dir.rename(old_dir)
        staging.rename(store_dir)
        if old_dir.exists():
            shutil.rmtree(old_dir)
