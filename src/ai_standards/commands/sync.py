from pathlib import Path

import typer

from ai_standards.adapters.claude_code import ClaudeCodeAdapter
from ai_standards.adapters.copilot import CopilotAdapter
from ai_standards.adapters.cursor import CursorAdapter
from ai_standards.adapters.shared import SharedAdapter
from ai_standards.detector import detect_languages
from ai_standards.store import CanonicalStore, NotInstalledError


def run(
    project_dir: Path,
    store_dir: Path,
    manifest_path: Path,
) -> None:
    try:
        store = CanonicalStore(store_dir, manifest_path)
    except NotInstalledError:
        typer.echo("Not installed. Run `ai-standards install` first.", err=True)
        raise typer.Exit(1)

    languages = detect_languages(project_dir, set())
    if "typescript" in languages:
        typer.echo(
            "TypeScript detected; no adapter available yet — deploying universal only"
        )
        languages = languages - {"typescript"}
    layers = store.assemble_layers(languages)
    skills = store.get_skills()

    SharedAdapter.run(project_dir, layers)
    ClaudeCodeAdapter.run(
        project_dir,
        layers,
        skills,
        reviewer_agent=store.get_content("content/claude/agents/code-reviewer.md"),
    )
    CursorAdapter.run(project_dir, layers, skills)
    CopilotAdapter.run(
        project_dir,
        layers,
        reviewer_agent=store.get_content("content/copilot/agents/reviewer.agent.md"),
        skills=skills,
    )
