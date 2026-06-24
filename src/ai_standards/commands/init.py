from pathlib import Path

import typer

from ai_standards.adapters.claude_code import ClaudeCodeAdapter
from ai_standards.adapters.copilot import CopilotAdapter
from ai_standards.adapters.cursor import CursorAdapter
from ai_standards.detector import detect_languages
from ai_standards.gitignore import GitignoreManager
from ai_standards.store import CanonicalStore, NotInstalledError


def run(
    project_dir: Path,
    store_dir: Path,
    manifest_path: Path,
    flags: set[str],
) -> None:
    try:
        store = CanonicalStore(store_dir, manifest_path)
    except NotInstalledError:
        typer.echo("Not installed. Run `ai-standards install` first.", err=True)
        raise typer.Exit(1)

    languages = detect_languages(project_dir, flags)

    if "typescript" in languages:
        typer.echo(
            "TypeScript detected; no adapter available yet — deploying universal only"
        )
        languages = languages - {"typescript"}

    layers = store.assemble_layers(languages)

    written: list[str] = []
    written.extend(ClaudeCodeAdapter.run(project_dir, layers))
    written.extend(
        CursorAdapter.run(
            project_dir,
            layers,
            skill_plan_task=store.get_content("content/skills/plan-task/SKILL.md"),
            skill_review=store.get_content("content/skills/review/SKILL.md"),
        )
    )
    written.extend(
        CopilotAdapter.run(
            project_dir,
            layers,
            reviewer_agent=store.get_content(
                "content/copilot/agents/reviewer.agent.md"
            ),
            review_prompt=store.get_content("content/skills/review/SKILL.md"),
        )
    )

    GitignoreManager.add_paths(project_dir / ".gitignore", written)
