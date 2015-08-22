#!/usr/bin/env make

WHICH_PYTHON := $(shell which python3)
VIRTUALENV := env
PYTHON := $(VIRTUALENV)/bin/python
PIP := $(VIRTUALENV)/bin/pip
APP := $(VIRTUALENV)/bin/dewbrick-app

$(VIRTUALENV):
	virtualenv -p $(WHICH_PYTHON) $(VIRTUALENV)

run: $(VIRTUALENV)
	$(APP)

build: $(VIRTUALENV)
	$(PYTHON) setup.py develop

clean:
	-rm -r env
	-rm -r *.egg*

.PHONY: build
.DEFAULT_GOAL := build
