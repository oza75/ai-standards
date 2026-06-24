import os
import subprocess
import tempfile
from pathlib import Path


def test_package_installable() -> None:
    project_root = Path(__file__).parent.parent.parent
    with tempfile.TemporaryDirectory() as tmp:
        result = subprocess.run(
            ["uv", "tool", "install", "--force", str(project_root)],
            capture_output=True,
            text=True,
            env={**os.environ, "UV_TOOL_DIR": tmp},
        )
        assert result.returncode == 0, result.stderr
