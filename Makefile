PYTHON_BIN ?= python

format:
	$(PYTHON_BIN) -m black .

test:
	$(PYTHON_BIN) -m pytest
