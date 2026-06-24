.PHONY: check test lint

check: lint
	uv run mypy src/ tests/
	uv run pytest

test:
	uv run pytest

lint:
	uv run ruff check src/ tests/
	uv run ruff format --check src/ tests/
