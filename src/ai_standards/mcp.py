"""Deploy the Context7 MCP server into each tool's MCP config.

Context7 (https://github.com/upstash/context7) serves up-to-date, version-specific
library documentation over MCP. It is deployed as a local stdio server via npx, with
no API key (the key is optional and only raises rate limits) — so nothing secret is
ever written to disk.

Each tool keeps its MCP config in a different file with a different top-level key, so
the per-tool wrapping is small but real. Writes MERGE into any existing config: a
project may already declare other MCP servers, and those must be preserved.
"""

import json
from pathlib import Path

CONTEXT7_COMMAND = "npx"
CONTEXT7_ARGS = ["-y", "@upstash/context7-mcp"]


def context7_server(*, include_type: bool) -> dict[str, object]:
    """The Context7 stdio server entry. `include_type` adds `type: stdio`.

    VS Code requires `type` on every server; Claude Code documents it; Cursor
    infers it from the presence of `command`, so it is omitted there.
    """
    server: dict[str, object] = {}
    if include_type:
        server["type"] = "stdio"
    server["command"] = CONTEXT7_COMMAND
    server["args"] = list(CONTEXT7_ARGS)
    return server


def merge_mcp_server(
    config_path: Path,
    top_level_key: str,
    server_name: str,
    server_spec: dict[str, object],
) -> None:
    """Merge one server entry into an MCP config file, preserving the rest.

    Reads the existing JSON if present, sets `[top_level_key][server_name]` to
    `server_spec`, and writes it back. Any other servers and any unrelated
    top-level fields are kept. Re-running with the same spec is a no-op in effect
    (idempotent output).
    """
    data: dict[str, object] = {}
    if config_path.exists():
        loaded = json.loads(config_path.read_text(encoding="utf-8"))
        if isinstance(loaded, dict):
            data = loaded

    servers = data.get(top_level_key)
    if not isinstance(servers, dict):
        servers = {}
        data[top_level_key] = servers
    servers[server_name] = server_spec

    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
