from pathlib import Path

import typer

from ai_standards.commands import sync as sync_cmd
from ai_standards.installer import Installer
from ai_standards.manifest import ManifestError, load_manifest


def run(
    project_dir: Path,
    store_dir: Path,
    manifest_path: Path,
) -> None:
    try:
        manifest = load_manifest(manifest_path)
    except ManifestError as exc:
        typer.echo(f"Error: {exc}", err=True)
        raise typer.Exit(1)

    try:
        Installer.run(manifest, store_dir)
    except Exception as exc:
        typer.echo(f"Update failed: {exc}", err=True)
        raise typer.Exit(1)

    sync_cmd.run(project_dir, store_dir, manifest_path)
