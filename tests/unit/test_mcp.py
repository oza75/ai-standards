import json
import tempfile
from pathlib import Path

from ai_standards.mcp import context7_server, merge_mcp_server


def test_creates_config_when_absent() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / ".mcp.json"

        merge_mcp_server(
            path, "mcpServers", "context7", context7_server(include_type=True)
        )

        data = json.loads(path.read_text(encoding="utf-8"))
        assert data["mcpServers"]["context7"]["command"] == "npx"
        assert data["mcpServers"]["context7"]["args"] == ["-y", "@upstash/context7-mcp"]
        assert data["mcpServers"]["context7"]["type"] == "stdio"


def test_include_type_false_omits_type() -> None:
    server = context7_server(include_type=False)
    assert "type" not in server
    assert server["command"] == "npx"


def test_preserves_existing_servers() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / ".mcp.json"
        path.write_text(
            json.dumps({"mcpServers": {"other": {"command": "foo"}}}),
            encoding="utf-8",
        )

        merge_mcp_server(
            path, "mcpServers", "context7", context7_server(include_type=False)
        )

        data = json.loads(path.read_text(encoding="utf-8"))
        assert data["mcpServers"]["other"] == {"command": "foo"}
        assert data["mcpServers"]["context7"]["command"] == "npx"


def test_preserves_unrelated_top_level_fields() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / ".vscode" / "mcp.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps({"inputs": [{"id": "x"}], "servers": {}}), encoding="utf-8"
        )

        merge_mcp_server(
            path, "servers", "context7", context7_server(include_type=True)
        )

        data = json.loads(path.read_text(encoding="utf-8"))
        assert data["inputs"] == [{"id": "x"}]
        assert data["servers"]["context7"]["type"] == "stdio"


def test_idempotent_output() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / ".mcp.json"

        merge_mcp_server(
            path, "mcpServers", "context7", context7_server(include_type=True)
        )
        first = path.read_bytes()
        merge_mcp_server(
            path, "mcpServers", "context7", context7_server(include_type=True)
        )
        second = path.read_bytes()

        assert first == second


def test_rewrites_non_dict_top_level_key() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / ".mcp.json"
        path.write_text(json.dumps({"mcpServers": "garbage"}), encoding="utf-8")

        merge_mcp_server(
            path, "mcpServers", "context7", context7_server(include_type=False)
        )

        data = json.loads(path.read_text(encoding="utf-8"))
        assert isinstance(data["mcpServers"], dict)
        assert data["mcpServers"]["context7"]["command"] == "npx"
