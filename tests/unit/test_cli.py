import subprocess
import sys


def test_cli_help_exits_zero() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "ai_standards", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "Usage" in result.stdout


def test_install_subcommand_listed_in_root_help() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "ai_standards", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "install" in result.stdout


def test_install_subcommand_help_exits_zero() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "ai_standards", "install", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0


def test_unknown_subcommand_exits_nonzero() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "ai_standards", "notacommand"],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
