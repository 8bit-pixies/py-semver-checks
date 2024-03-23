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
	@pytest --cov . tests/
