VENV = .venv
VIRTUALENV = virtualenv
BIN = $(VENV)/bin
PYTHON = $(BIN)/python

INSTALL = $(BIN)/pip install

.PHONY: all dist build

all: build

$(PYTHON):
	$(VIRTUALENV) $(VTENV_OPTS) $(VENV)

build: $(PYTHON)
	$(PYTHON) setup.py develop

dist:
	$(INSTALL) wheel
	$(PYTHON) setup.py sdist bdist_wheel

clean:
	rm -rf $(VENV)

