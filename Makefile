markdown_lint:
	markdownlint --disable MD013 MD033 MD041 --fix . --ignore CODE_OF_CONDUCT.md

ruff_lint:
	uv run ruff format
	uv run ruff check --fix

ruff_check:
	uv run ruff check

ruff_format_check:
	uv run ruff format --check

install:
	uv sync --locked --all-extras --dev

build:
	uv build --no-sources

update:
	uv lock --upgrade

upgrade: update install

test: ruff_format_check ruff_check
	uv run pytest -vv --cov=./ --cov-report html --cov-report=lcov --cov-branch -n auto
