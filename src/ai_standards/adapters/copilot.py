from pathlib import Path

# Pinned from pre-coding gate: GitHub Copilot bare-name tool reference,
# retrieved 2026-06-24 (https://docs.github.com/en/copilot/reference/custom-agents-configuration).
# Authoritative over VS Code namespaced format for .github/agents/*.agent.md files.
REVIEWER_AGENT_TOOLS: list[str] = ["read", "search"]


class CopilotAdapter:
    @staticmethod
    def run(
        project_dir: Path,
        layers: dict[str, str],
        reviewer_agent: str,
        skills: dict[str, str],
    ) -> list[str]:
        github_dir = project_dir / ".github"

        ci = github_dir / "copilot-instructions.md"
        ci.parent.mkdir(parents=True, exist_ok=True)
        ci.write_text(layers["universal"], encoding="utf-8")

        agents_dir = github_dir / "agents"
        agents_dir.mkdir(parents=True, exist_ok=True)
        (agents_dir / "reviewer.agent.md").write_text(reviewer_agent, encoding="utf-8")

        written: list[str] = [
            ".github/copilot-instructions.md",
            ".github/agents/reviewer.agent.md",
        ]

        prompts_dir = github_dir / "prompts"
        prompts_dir.mkdir(parents=True, exist_ok=True)
        for name, content in skills.items():
            (prompts_dir / f"{name}.prompt.md").write_text(content, encoding="utf-8")
            written.append(f".github/prompts/{name}.prompt.md")

        return written
