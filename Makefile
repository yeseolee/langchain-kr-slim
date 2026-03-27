PYTHON := .venv/bin/python
RUFF := .venv/bin/ruff
PY_FILES := src/langchain_cookbook/openrouter_setup.py

.PHONY: sync format lint check

sync:
	uv sync

format:
	$(RUFF) format $(PY_FILES)
	$(RUFF) check --fix $(PY_FILES)

lint:
	$(RUFF) check $(PY_FILES)

check: format lint
