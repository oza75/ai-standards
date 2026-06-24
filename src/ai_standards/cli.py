import typer

app = typer.Typer(no_args_is_help=True)


@app.callback()
def main() -> None:
    """Manage personal AI coding standards across Claude Code, Cursor, and Copilot."""


@app.command()
def install() -> None:
    """Download canonical layer files from GitHub to ~/.ai-standards/."""
    raise NotImplementedError("install command not yet implemented — run STD-6")
