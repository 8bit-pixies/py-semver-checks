.PHONY: format format-only lint test

format:
	@ruff format
	@ruff . --fix

format-only:
	@ruff format

lint:
	@ruff .
	@mypy

test:
	@pytest --cov . --verbose --color=yes --cov-report=term-missing:skip-covered tests/
