import importlib.resources
from pathlib import Path

import typer

from ai_standards.commands import init as init_cmd
from ai_standards.commands import sync as sync_cmd
from ai_standards.commands import update as update_cmd
from ai_standards.installer import Installer
from ai_standards.manifest import ManifestError, load_manifest

app = typer.Typer(no_args_is_help=True)

_STORE_DIR = Path.home() / ".ai-standards"


@app.callback()
def main() -> None:
    """Manage personal AI coding standards across Claude Code, Cursor, and Copilot."""


@app.command()
def install() -> None:
    """Download canonical layer files from GitHub to ~/.ai-standards/."""
    ref = importlib.resources.files("ai_standards") / "manifest.json"
    with importlib.resources.as_file(ref) as manifest_path:
        try:
            manifest = load_manifest(manifest_path)
        except ManifestError as exc:
            typer.echo(f"Error: {exc}", err=True)
            raise typer.Exit(1)

    typer.echo("Installing ai-standards…")
    try:
        Installer.run(manifest, _STORE_DIR)
    except Exception as exc:
        typer.echo(f"Install failed: {exc}", err=True)
        raise typer.Exit(1)

    typer.echo(f"Installed to {_STORE_DIR}")


@app.command()
def init(
    python: bool = typer.Option(False, "--python", help="Force Python layer."),
    typescript: bool = typer.Option(
        False, "--typescript", help="Force TypeScript layer."
    ),
) -> None:
    """Detect language, deploy all adapters, and update .gitignore."""
    flags: set[str] = set()
    if python:
        flags.add("python")
    if typescript:
        flags.add("typescript")

    ref = importlib.resources.files("ai_standards") / "manifest.json"
    with importlib.resources.as_file(ref) as manifest_path:
        init_cmd.run(Path.cwd(), _STORE_DIR, manifest_path, flags)
    typer.echo("Done.")


@app.command()
def sync() -> None:
    """Re-deploy all adapter files from ~/.ai-standards/ to the current project."""
    ref = importlib.resources.files("ai_standards") / "manifest.json"
    with importlib.resources.as_file(ref) as manifest_path:
        sync_cmd.run(Path.cwd(), _STORE_DIR, manifest_path)
    typer.echo("Done.")


@app.command()
def update() -> None:
    """Re-download canonical files from GitHub, then re-deploy to current project."""
    ref = importlib.resources.files("ai_standards") / "manifest.json"
    with importlib.resources.as_file(ref) as manifest_path:
        update_cmd.run(Path.cwd(), _STORE_DIR, manifest_path)
    typer.echo("Done.")
