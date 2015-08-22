#!/usr/bin/env make

WHICH_PYTHON := $(shell which python3)
VIRTUALENV := env
PYTHON := $(VIRTUALENV)/bin/python
PIP := $(VIRTUALENV)/bin/pip

$(VIRTUALENV):
	virtualenv -p $(WHICH_PYTHON) $(VIRTUALENV)

build: $(VIRTUALENV)
	$(PIP) install -r requirements.txt

clean:
	-rm -r env

.PHONY: build
.DEFAULT_GOAL := build
