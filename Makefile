.PHONY: all test run lint clean

### Default target(s)
all: test

### Clean up generated files
clean:
	uv clean
	rm -fr .ruff_cache .venv

### Install this tool locally
install:
	uv tool install --upgrade .

### Perform static analysis
lint:
	uv tool run ruff check --select I --fix .
	uv tool run ruff format .
	uv tool run ruff check . --fix

### Run unit tests
test: lint
	uv run pytest -s -v

### Display in tree format
tree: lint
	uv run ntree src/test/data/nginx.conf | less